# Chall - Terminal Access

> Simple IDOR to Account Takeover

## Challenge Type

- [ ] **OFF**line
- [X] **ON**line

## Design Type

- [X] **Black**-Box
- [ ] **White**-Box

## Designer

- Harsh Sawant

## Description

A IDOR web challenge, during login, after credential check request, another request is sent where an id is taken from the client and the session is set for that id user, however it is not checked whether the credentials used belong to the id of the user passed or not, thus creating a condition where a single pair of correct credentials can let a user access any other user's data.  

The goal is to help develop a beginner participant's intuition about insecure login flows, and testing all requests that the client makes to the server, even the ones that are not directly visible or apparent to a user.

## Category

- `web`

---
