import json
import math
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from .http import json_request
from .models import DIMENSIONS, MODEL, MODEL_REVISION, PROFILE, KnowledgeError


def validate_vectors(vectors, count):
    if not isinstance(vectors, list) or len(vectors) != count:
        raise KnowledgeError("Embedding count does not match the requested texts")
    for vector in vectors:
        if not isinstance(vector, list) or len(vector) != DIMENSIONS:
            raise KnowledgeError("Embedding dimension does not match the index profile")
        if not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
                   for v in vector):
            raise KnowledgeError("Embedding contains invalid values")
        if sum(v * v for v in vector) < 1e-12:
            raise KnowledgeError("Embedding cannot be a zero vector")
    return vectors


class LocalEmbedder:
    profile = PROFILE

    def __init__(self):
        self._model = None
        self._lock = threading.Lock()

    def encode(self, texts):
        if not texts:
            return []
        with self._lock:
            if self._model is None:
                try:
                    from sentence_transformers import SentenceTransformer
                    self._model = SentenceTransformer(
                        MODEL, revision=MODEL_REVISION, device="cpu", trust_remote_code=False
                    )
                except ImportError:
                    raise KnowledgeError(
                        "Install the knowledge embeddings extra in the worker"
                    ) from None
                except Exception:
                    raise KnowledgeError(
                        "Cannot load the pinned BGE-M3 model in the worker"
                    ) from None
            try:
                # Refuse silent tokenizer truncation if configuration drifts.
                for text in texts:
                    tokens = self._model.tokenizer.encode(text, add_special_tokens=True)
                    if len(tokens) > self._model.max_seq_length:
                        raise KnowledgeError("Text exceeds the embedding model context window")
                vectors = self._model.encode(texts, batch_size=4, normalize_embeddings=True,
                                             show_progress_bar=False).tolist()
            except KnowledgeError:
                raise
            except Exception:
                raise KnowledgeError("Local embedding inference failed") from None
        return validate_vectors(vectors, len(texts))


class HttpEmbedder:
    profile = PROFILE

    def __init__(self, url="http://127.0.0.1:8091"):
        parsed = urlparse(url)
        # V1 is local only; model inputs are not sent to arbitrary remote services.
        if parsed.scheme != "http" or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise KnowledgeError("The embedding worker URL must use loopback HTTP")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise KnowledgeError(
                "The embedding worker URL must not contain credentials or parameters"
            )
        self.url = url.rstrip("/")

    def encode(self, texts):
        if not texts:
            return []
        result = json_request(self.url + "/embed", body={"texts": texts}, timeout=180)
        if result.get("profile") != self.profile:
            raise KnowledgeError(
                "Embedding worker and index profiles differ; reindex before serving"
            )
        return validate_vectors(result.get("vectors"), len(texts))


def embedding_server(embedder, port=8091):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass  # Do not log queries or document text.

        def respond(self, status, body):
            payload = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            self.respond(200 if self.path == "/health" else 404,
                         {"service": "knowledge-embeddings", "profile": PROFILE})

        def do_POST(self):
            if self.path != "/embed":
                self.respond(404, {"detail": "Not found"})
                return
            # Browser pages cannot use the private worker as a cross-origin inference endpoint.
            if self.headers.get("Origin"):
                self.respond(403, {"detail": "Browser origins are not allowed"})
                return
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 200_000:
                    raise ValueError
                if self.headers.get_content_type() != "application/json":
                    raise ValueError
                self.connection.settimeout(30)
                body = json.loads(self.rfile.read(size))
                texts = body["texts"]
                if (not isinstance(texts, list) or not 1 <= len(texts) <= 32
                    or not all(isinstance(t, str) and 0 < len(t) <= 12_000 for t in texts)):
                    raise ValueError
                self.respond(200, {"profile": embedder.profile, "vectors": embedder.encode(texts)})
            except (ValueError, KeyError, TypeError, TimeoutError):
                self.respond(400, {"detail": "Expected 1-32 bounded, nonempty texts as JSON"})
            except KnowledgeError as exc:
                self.respond(503, {"detail": str(exc)})

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)
