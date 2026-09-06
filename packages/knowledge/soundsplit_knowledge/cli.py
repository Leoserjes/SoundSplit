import argparse
import json
import os

from .embeddings import HttpEmbedder, LocalEmbedder, embedding_server
from .models import KnowledgeError
from .notion import NotionReader, read_token
from .store import PostgresStore
from .sync import synchronize

DEFAULT_ROOT = "3d381a9a-01d0-811a-beb0-d6bcd51cc668"


def database_url() -> str:
    return os.getenv(
        "KNOWLEDGE_DATABASE_URL",
        os.getenv("DATABASE_URL", "postgresql://soundsplit:soundsplit@localhost:5432/soundsplit"),
    )


def parser():
    result = argparse.ArgumentParser(description="SoundSplit Knowledge Retrieval operations")
    commands = result.add_subparsers(dest="command", required=True)
    commands.add_parser("init-db", help="Create the rebuildable pgvector index")
    sync = commands.add_parser("sync", help="Synchronize the configured Notion page tree")
    sync.add_argument("--root", default=os.getenv("NOTION_KNOWLEDGE_ROOT_ID", DEFAULT_ROOT))
    sync.add_argument("--mcp-config", help="Explicit local MCP config fallback for NOTION_TOKEN")
    sync.add_argument("--embedding-url", default=os.getenv("KNOWLEDGE_EMBEDDING_URL",
                                                           "http://127.0.0.1:8091"))
    sync.add_argument("--force", action="store_true", help="Re-embed every document")
    worker = commands.add_parser("serve-embeddings", help="Run the loopback-only BGE-M3 worker")
    worker.add_argument("--port", type=int, default=8091)
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "init-db":
            PostgresStore(database_url()).initialize()
            result = {"status": "initialized"}
        elif args.command == "serve-embeddings":
            if not 1 <= args.port <= 65535:
                raise KnowledgeError("Port must be between 1 and 65535")
            embedding_server(LocalEmbedder(), args.port).serve_forever()
            return 0
        else:
            token = read_token(args.mcp_config)
            store = PostgresStore(database_url())
            result = synchronize(NotionReader(token), store, HttpEmbedder(args.embedding_url),
                                 args.root, force=args.force)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        return 0
    except KnowledgeError as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
