+++
date = "2017-06-08T00:00:00Z"
tags = ["github","javascript"]
title = "HyperApp - 1kb JavaScript library for building frontend applications."

+++

> HyperApp is a JavaScript library for building frontend applications.<!--more-->

- Declarative: HyperApp's design is based on the Elm Architecture. Create scalable browser-based applications using a functional paradigm. The twist is you don't have to learn a new language.
- Custom tags: Build complex user interfaces from custom tags. Custom tags are stateless, framework agnostic and easy to debug.
- Batteries-included: Out of the box, HyperApp has Elm-like state management and a virtual DOM engine; it still weighs 1kb and has no dependencies.

#### Hello World
```
app({
  state: 0,
  view: (state, actions) => (
    <main>
      <h1>{state}</h1>
      <button onclick={actions.add}>+</button>
      <button onclick={actions.sub}>-</button>
    </main>
  ),
  actions: {
    add: state => state + 1,
    sub: state => state - 1
  }
})
```

#### Documentation
The documentation is located in the [docs](https://github.com/hyperapp/hyperapp/blob/master/docs) directory.