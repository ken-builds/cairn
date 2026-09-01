import assert from "node:assert/strict";
import test from "node:test";

import { identity } from "./index.js";

test("identity returns its input", () => {
  assert.equal(identity("cairn"), "cairn");
});
