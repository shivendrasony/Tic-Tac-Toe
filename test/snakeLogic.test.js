import test from "node:test";
import assert from "node:assert/strict";

import {
  createInitialState,
  placeFood,
  queueDirection,
  stepGame
} from "../src/snakeLogic.js";

test("moves snake in the queued direction", () => {
  let state = createInitialState(() => 0);
  state = queueDirection(state, "right");
  state = stepGame(state, () => 0);

  assert.deepEqual(state.snake[0], { x: 9, y: 8 });
  assert.equal(state.score, 0);
  assert.equal(state.isGameOver, false);
});

test("grows snake and increments score after eating food", () => {
  let state = createInitialState(() => 0);
  state = {
    ...state,
    hasStarted: true,
    food: { x: 9, y: 8 }
  };

  const nextState = stepGame(state, () => 0);

  assert.equal(nextState.snake.length, state.snake.length + 1);
  assert.equal(nextState.score, 1);
  assert.notDeepEqual(nextState.food, { x: 9, y: 8 });
});

test("ends the game when the snake hits a wall", () => {
  const state = {
    ...createInitialState(() => 0, 4),
    hasStarted: true,
    direction: "right",
    pendingDirection: "right",
    snake: [
      { x: 3, y: 1 },
      { x: 2, y: 1 },
      { x: 1, y: 1 }
    ],
    food: { x: 0, y: 0 }
  };

  const nextState = stepGame(state, () => 0);

  assert.equal(nextState.isGameOver, true);
});

test("ends the game when the snake collides with itself", () => {
  const state = {
    ...createInitialState(() => 0, 6),
    hasStarted: true,
    direction: "up",
    pendingDirection: "left",
    snake: [
      { x: 2, y: 2 },
      { x: 2, y: 3 },
      { x: 1, y: 3 },
      { x: 1, y: 2 },
      { x: 1, y: 1 },
      { x: 2, y: 1 }
    ],
    food: { x: 5, y: 5 }
  };

  const nextState = stepGame(state, () => 0);

  assert.equal(nextState.isGameOver, true);
});

test("places food only on empty cells", () => {
  const food = placeFood(
    [
      { x: 0, y: 0 },
      { x: 1, y: 0 },
      { x: 0, y: 1 }
    ],
    2,
    () => 0
  );

  assert.deepEqual(food, { x: 1, y: 1 });
});

test("prevents reversing directly into the snake body", () => {
  const state = {
    ...createInitialState(() => 0),
    hasStarted: true,
    direction: "right",
    pendingDirection: "right"
  };

  const nextState = queueDirection(state, "left");

  assert.equal(nextState.pendingDirection, "right");
});
