+++
date = "2021-06-21T09:57:26+08:00"
tags = ["github","javascript","react"]
title = "react-flight - build animation compositions for React"

+++

> [react-flight](https://github.com/jondot/react-flight) is the best way to build animation compositions for React.<!--more-->

![](https://github.com/jondot/react-flight/raw/master/media/flight.png)

### [official website](http://react-flight.io)

Check out the new video:
<br/>
<a href="https://youtu.be/HBEn-KN_u04">
<img src="https://i.ytimg.com/vi/HBEn-KN_u04/hqdefault.jpg" width="240"/>
<br/>
React Flight in Three Minutes
</a>

## Quick Start (From Scratch)

Just clone and use the example, built around `create-react-app`:

```
$ git clone https://github.com/jondot/react-flight
$ cd react-flight/examples/compos
$ yarn && yarn start
```


## Quick Start (Existing Project)

With yarn (or npm):

```
$ yarn add react-flight
$ curl https://raw.githubusercontent.com/jondot/react-flight/master/examples/compos/src/index.js -o src/anim.js
```

And now you can frame your compositions in `anim.js`, require and place it in
any other React component.

Next:

1. Add jQuery (or Zepto, or any jQuery drop-in) if you don't have it already in the project.
2. Or if you use `create-react-app` you can add it to your `public/index.html`, [like here](examples/compos/public/index.html),
or eject and [configure webpack](https://webpack.github.io/docs/library-and-externals.html) for jQuery.

_NOTE_: jQuery is currently a requirement of one of `react-flight`'s dependencies.
We plan to rebuild that dependency any way, obsoleting this requirement in the
process (also: PRs accepted!).

## Workflow

When you're designing compositions, focus on designing frames. The
first frame is marked `source` because that's the starting point, and
`interactive` because you want to play with it while you go.

```jsx
  <Flight interactive ref={flight => (this.flight = flight)}>
    <Flight.Frame duration={300} source interactive showFrames>
```

### Showing Frames

While designing, you want to have `showFrames` on. It will unpack
all of the frames in front of you, so you could edit them while watching them. With
Webpack hot-reload this becomes a fantastic experience.

When done, remove `showFrames`.

### Controlling Flight Directly

This is where the `ref` addition comes in:

```jsx
  <Flight interactive ref={flight => (this.flight = flight)}>
    <Flight.Frame duration={300} source interactive showFrames>
```

Once you can grab an instance of `flight` you can `flight.play()` and `flight.reset()` on
demand from your own components and actions.

Here's a full layout:

```jsx
  <Flight interactive ref={flight => (this.flight = flight)}>
    <Flight.Frame duration={300} source interactive showFrames>

      -- your own DOM / React Components ---
      -- starting position and styles    ---

    </Flight.Frame>

    <Flight.Frame>

      -- your own DOM / React Components ---
      -- ending position and styles    ---

    </Flight.Frame>
  </Flight>
```





## Redux

If you're using Redux, there's basic support for it. Basic in the sense that `react-flight` is not
going to handle deep renders of a stateful app with all its gotchas, so YMMV.

You can check out [this Redux example](examples/compos-redux) for a fully working solution.


For your app, you can enable Redux support by indicating inclusion of store before using the `Flight` component:

```javascript
Flight.contextTypes = {
  store: PropTypes.object,
}

Flight.childContextTypes = {
  ...Flight.childContextTypes,
  store: PropTypes.object,
}
```



