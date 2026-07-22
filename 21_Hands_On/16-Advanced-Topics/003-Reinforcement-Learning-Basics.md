# 003 - Reinforcement Learning Basics

## Concept
Reinforcement Learning (RL) trains an agent to make sequential decisions by interacting with an environment: it takes actions, receives rewards, and learns a policy that maximizes cumulative reward over time — fundamentally different from supervised learning's fixed labeled examples.

## Why It Matters
RL is behind game-playing AI (AlphaGo), robotics control, and is also a core ingredient in RLHF, the technique used to align modern LLMs (module 16-002) with human preferences.

## Hands-On

```python
# pip install gymnasium numpy --break-system-packages
import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt

# 1. The RL loop: agent takes actions, environment returns (next_state, reward, done)
env = gym.make("FrozenLake-v1", is_slippery=False)  # simple grid-world environment
state, info = env.reset()
print("Observation space:", env.observation_space)   # 16 discrete grid cells
print("Action space:", env.action_space)              # 4 discrete actions (up/down/left/right)

# 2. Q-Learning - learns a table of Q(state, action) values via trial and error
n_states = env.observation_space.n
n_actions = env.action_space.n
Q = np.zeros((n_states, n_actions))

alpha = 0.8         # learning rate
gamma = 0.95        # discount factor - how much future rewards matter vs immediate ones
epsilon = 1.0        # exploration rate - starts high, decays over training
epsilon_decay = 0.995
epsilon_min = 0.01
n_episodes = 2000

rewards_per_episode = []

for episode in range(n_episodes):
    state, _ = env.reset()
    total_reward = 0
    done = False

    while not done:
        # Epsilon-greedy action selection: explore randomly or exploit best known action
        if np.random.rand() < epsilon:
            action = env.action_space.sample()        # explore
        else:
            action = np.argmax(Q[state])                # exploit

        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated

        # The Q-learning update rule (Bellman equation)
        best_next_q = np.max(Q[next_state])
        Q[state, action] += alpha * (reward + gamma * best_next_q - Q[state, action])

        state = next_state
        total_reward += reward

    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    rewards_per_episode.append(total_reward)

# 3. Plot learning progress - average reward should trend upward
window = 100
moving_avg = [np.mean(rewards_per_episode[max(0, i-window):i+1]) for i in range(len(rewards_per_episode))]
plt.plot(moving_avg)
plt.xlabel("Episode")
plt.ylabel(f"Average reward (last {window} episodes)")
plt.title("Q-Learning Progress on FrozenLake")
plt.savefig("qlearning_progress.png")
plt.close()

print(f"Average reward, last 100 episodes: {np.mean(rewards_per_episode[-100:]):.2f}")

# 4. Inspect the learned policy
print("\nLearned Q-table (state x action):")
print(np.round(Q, 2))

action_names = ["Left", "Down", "Right", "Up"]
policy = [action_names[np.argmax(Q[s])] for s in range(n_states)]
print("\nLearned policy (best action per state):", policy)

# 5. Evaluate the trained (greedy) policy with no exploration
def evaluate_policy(Q, env, n_episodes=100):
    successes = 0
    for _ in range(n_episodes):
        state, _ = env.reset()
        done = False
        while not done:
            action = np.argmax(Q[state])
            state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            if terminated and reward == 1:
                successes += 1
    return successes / n_episodes

success_rate = evaluate_policy(Q, env)
print(f"\nSuccess rate with learned policy: {success_rate:.2%}")
```

## Exercise
1. Set `is_slippery=True` (stochastic environment) and re-train — how does the learned policy and success rate change compared to the deterministic version?
2. Experiment with different `gamma` values (0.5 vs 0.99) — how does the agent's behavior change when it values immediate vs. long-term rewards differently?
3. Implement a random-action baseline (no learning) and compare its success rate to the trained Q-learning agent's.

## Key Takeaways
- RL has no fixed labeled dataset — the agent generates its own experience through trial and error, guided only by a reward signal.
- The exploration-exploitation trade-off (epsilon-greedy here) is central to RL: too much exploration wastes time on bad actions, too little means missing better strategies.
- Q-learning's tabular approach only scales to small, discrete state spaces — real-world problems with huge or continuous state spaces (like Atari games or robotics) need deep RL, which replaces the Q-table with a neural network (Deep Q-Networks and beyond).
