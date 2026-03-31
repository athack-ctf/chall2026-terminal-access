# @Hack 2026: Terminal Access

> Authored by [Harsh](https://github.com/sudo-i-u-harsh11235).

- **Category**: `Web`
- **Solves**: `54/120`
- **Tags**: `beginner`
- **Protocol**: `http`

> The Aliens have planted hidden terminals everywhere! We've found one of the them, but it is protected by some
> authentication mechanism.
>
> Bypass it and help us get their secrets!
>

## Access a dockerized instance

Run challenge container using docker compose

```
docker compose up -d
```

Open below URL on your browser

```
http://localhost:53022/
```

<details>
<summary>
How to stop/restart challenge?
</summary>

To stop the challenge run

```
docker compose stop
```

To restart the challenge run

```
docker compose restart
```

</details>

## Reveal Flag(s)

Did you try solving this challenge?
<details>
<summary>
Yes
</summary>

Did you **REALLY** try solving this challenge?

<details>
<summary>
Yes, I promise!
</summary>

- Flag 1: `ATHACKCTF{1n53cur3_d1r3c7_4l13n_r3f3r3nc3}`

</details>
</details>


---

## About @Hack

[@Hack](https://athackctf.com/) is an annual CTF (Capture The Flag) competition hosted
by [HEXPLOIT ALLIANCE](https://hexploit-alliance.com/) and [TECHNATION](https://technationcanada.ca/) at Concordia
University in Montreal, Canada.

---
[Check more challenges from @Hack 2026](https://github.com/athack-ctf/AtHackCTF-2026-Challenges).
