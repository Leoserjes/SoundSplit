import "@testing-library/jest-dom/vitest";

import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("renders the initial harmonIA analysis workspace", () => {
    render(<App />);

    expect(screen.getByText("SoundSplit")).toBeInTheDocument();
    expect(screen.getByText("harmonIA")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "New music analysis" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Run analysis" })).toBeInTheDocument();
    expect(screen.getByLabelText("Audio import area")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Expected outputs" })).toBeInTheDocument();
  });
});
