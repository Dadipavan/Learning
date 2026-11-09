import numpy as np
N, gamma = 4, 0.9
MOVES = [(-1, 0), (1, 0), (0, -1), (0, 1)]   # up, down, left, right
def step(s, a):
    r, c = s[0] + MOVES[a][0], s[1] + MOVES[a][1]
    if not (0 <= r < N and 0 <= c < N): r, c = s
    if (r, c) == (3, 3): return (r, c), 10.0, True
    if (r, c) == (1, 1): return (r, c), -10.0, True
    return (r, c), -1.0, False

def softmax(z):
    e = np.exp(z - z.max()); return e / e.sum()

def reinforce(seed, episodes=3000, lr=0.05, baseline=False):
    rng = np.random.default_rng(seed)
    theta = np.zeros((N, N, 4)); b = np.zeros((N, N))   # b: running mean return per state
    rets = []
    for ep in range(episodes):
        s, traj = (0, 0), []
        for t in range(60):
            p = softmax(theta[s]); a = rng.choice(4, p=p)
            ns, rw, d = step(s, a); traj.append((s, a, rw)); s = ns
            if d: break
        G, Gs = 0.0, []
        for (_, _, rw) in reversed(traj):
            G = rw + gamma * G; Gs.append(G)
        Gs.reverse()
        for (s_, a_, _), G_ in zip(traj, Gs):
            adv = G_ - (b[s_] if baseline else 0.0)
            g = -softmax(theta[s_]); g[a_] += 1
            theta[s_] += lr * adv * g
            if baseline: b[s_] += 0.1 * (G_ - b[s_])
        rets.append(sum(rw for _, _, rw in traj))
    return theta, np.array(rets)

for base in (False, True):
    last = []
    for seed in range(10):
        _, r = reinforce(seed, baseline=base); last.append(r[-200:].mean())
    print("baseline   " if base else "no baseline", "per-seed mean return, last 200 episodes:", np.round(last, 1))
    print("            mean %.2f, std across seeds %.2f" % (np.mean(last), np.std(last)))
