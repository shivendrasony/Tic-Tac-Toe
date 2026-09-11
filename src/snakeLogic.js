export const GRID_SIZE = 16;
export const INITIAL_DIRECTION = "right";
export const DIRECTIONS = {
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 }
};

const OPPOSITES = {
  up: "down",
  down: "up",
  left: "right",
  right: "left"
};

export function createInitialState(random = Math.random, size = GRID_SIZE) {
  const center = Math.floor(size / 2);
  const snake = [
    { x: center, y: center },
    { x: center - 1, y: center },
    { x: center - 2, y: center }
  ];

  return {
    size,
    snake,
    direction: INITIAL_DIRECTION,
    pendingDirection: INITIAL_DIRECTION,
    food: placeFood(snake, size, random),
    score: 0,
    isGameOver: false,
    isPaused: false,
    hasStarted: false
  };
}

export function placeFood(snake, size, random = Math.random) {
  const occupied = new Set(snake.map(toKey));
  const available = [];

  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const cell = { x, y };
      if (!occupied.has(toKey(cell))) {
        available.push(cell);
      }
    }
  }

  if (available.length === 0) {
    return null;
  }

  const index = Math.floor(random() * available.length);
  return available[index];
}

export function queueDirection(state, nextDirection) {
  if (!DIRECTIONS[nextDirection] || state.isGameOver) {
    return state;
  }

  const activeDirection = state.hasStarted ? state.direction : state.pendingDirection;
  if (OPPOSITES[activeDirection] === nextDirection) {
    return state;
  }

  return {
    ...state,
    pendingDirection: nextDirection,
    hasStarted: true
  };
}

export function togglePause(state) {
  if (state.isGameOver || !state.hasStarted) {
    return state;
  }

  return {
    ...state,
    isPaused: !state.isPaused
  };
}

export function stepGame(state, random = Math.random) {
  if (state.isGameOver || state.isPaused || !state.hasStarted) {
    return state;
  }

  const direction = state.pendingDirection;
  const move = DIRECTIONS[direction];
  const head = state.snake[0];
  const nextHead = {
    x: head.x + move.x,
    y: head.y + move.y
  };

  const hitsWall =
    nextHead.x < 0 ||
    nextHead.y < 0 ||
    nextHead.x >= state.size ||
    nextHead.y >= state.size;
  if (hitsWall) {
    return {
      ...state,
      direction,
      isGameOver: true
    };
  }

  const willEat = state.food && nextHead.x === state.food.x && nextHead.y === state.food.y;
  const nextSnake = [nextHead, ...state.snake];
  if (!willEat) {
    nextSnake.pop();
  }

  const bodyToCheck = nextSnake.slice(1);
  const hitsSelf = bodyToCheck.some((segment) => segment.x === nextHead.x && segment.y === nextHead.y);
  if (hitsSelf) {
    return {
      ...state,
      direction,
      isGameOver: true
    };
  }

  return {
    ...state,
    snake: nextSnake,
    direction,
    food: willEat ? placeFood(nextSnake, state.size, random) : state.food,
    score: willEat ? state.score + 1 : state.score
  };
}

function toKey(cell) {
  return `${cell.x},${cell.y}`;
}
