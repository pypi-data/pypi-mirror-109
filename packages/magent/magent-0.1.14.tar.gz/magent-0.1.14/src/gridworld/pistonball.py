from pettingzoo.butterfly import pistonball_v1
import numpy as np
import sys
import time
import random
from pettingzoo.utils.observation_saver import save_observation

GRAYSCALE_WEIGHTS = np.array([0.299, 0.587, 0.114], dtype=np.float32)

print(GRAYSCALE_WEIGHTS@np.array([68,76,77]))
def change_observation(obs):
    obs = (obs.astype(np.float32) @ GRAYSCALE_WEIGHTS).astype(np.uint8)
    return obs

DOWN = 0
UP = 2
HOLD = 1

count = 0
def policy(env, agent, obs):
    global count
    obs = change_observation(obs)
    # obs = obs[:100,:]
    count += 1
    # if agent == "piston_1":
    #     save_observation(env, agent,save_dir=f"saves/{count}")
    ball_vals = np.equal(obs, 137)
    first_loc = np.argmax(ball_vals,axis=1)
    if first_loc.any():
        first_loc_nonzero = np.where(first_loc == 0, 1000, first_loc)
        min_loc = np.min(first_loc_nonzero)
        max_loc = np.max(first_loc)
        if min_loc < 5:
            return UP
        elif max_loc > 80:
            return DOWN
        else:
            return HOLD#UP if random.random() < 0.5 else HOLD

    first_piston_vals = np.equal(obs,73)#.astype(np.int32)
    uniques, counts = np.unique(obs,return_counts=True)
    # time.sleep(0.01)
    pi1 = 200 - np.argmax(first_piston_vals[:,11])
    pi2 = 200 - np.argmax(first_piston_vals[:,51])
    pi3 = 200 - np.argmax(first_piston_vals[:,91])
    print(agent, pi1,pi2,pi3)
    if pi1 == 200:
        action = DOWN
    elif pi3 == 200:
        action = UP
    else:
        return DOWN
        if pi2 > pi3:
            action = DOWN
        elif pi1 > pi2:
            action = UP
        elif pi1 + 1 < pi2:
            action = DOWN
        elif pi2 + 16 < pi3:
            action = UP
        else:
            action = UP

    return action

def main(render=False):
    env = pistonball_v1.env()
    total_reward = 0
    NUM_RESETS = 1
    for i in range(NUM_RESETS):
        # env.seed(112123123)
        env.reset()
        # env.step(1)
        # env.reset()
        for agent in env.agent_iter():
            obs, rew, done, info = env.last()
            act = policy(env,agent,obs) if not done else None
            env.step(act)
            total_reward += rew
            if render:
                env.render()

    env.close()
    print("average total reward: ",total_reward/NUM_RESETS)

if __name__ == "__main__":
    render = len(sys.argv) > 1 and sys.argv[1] == "render"
    main(render)
