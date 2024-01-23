## A working example

```xml
  <path

      stroke="#848cc8"
      stroke-width="0.5"
      stroke-dasharray="363.0335388183594"
      stroke-opacity="1"
      fill="none"
      stroke-dashoffset="363.0335388183594"

     d="....hmm interesting path info 6969..."
     id="text-part"
     aria-label="Blueberry" />

     <animate
         id="stroke-animation"
         xlink:href="#text-part" 
         attributeName="stroke-dashoffset"
         values="363.0335388183594;0"
         dur="3s"
         keyTimes="0;1"
         calcMode="spline"
         keySplines="0.47 0 0.745 0.715"
         repeatCount="1"
         fill="freeze"
    />

    <animate
         id="fill-animation"
         xlink:href="#text-part" 
         attributeName="fill"
         values="transparent;rgb(132, 140, 200)"
         dur="0.7s"
         keyTimes="0;1"
         calcMode="spline"
         keySplines="0.47, 0, 0.745, 0.715"
         begin="0.8s" fill="freeze"
    />
```
is basically this:
```css
 svg .svg-elem-1 {
  /* initial state */
  stroke-dashoffset: 363.0335388183594px;
  stroke-dasharray: 363.0335388183594px;
  fill: transparent;

  /* the transition itself */
  transition: stroke-dashoffset 1s cubic-bezier(0.47, 0, 0.745, 0.715) 0s,
    fill 0.7s cubic-bezier(0.47, 0, 0.745, 0.715) 0.8s;

    /* ..and you can have other properties and so on... */
}

svg.active .svg-elem-1 {
  /* final state */
  stroke-dashoffset: 0;
  fill: rgb(132, 140, 200);
}
```

`keytimes` denotes the part where you have `1s cubic-bezier .. 0s`

`spline` === `cubic-bezier`
and `keySplines` is the stuff that goes into the `cubic-bezier` function

## cool stuff I came across
- https://css-tricks.com/guide-svg-animations-smil/#why-use-svg-animations
- https://shapeshifter.design/ 
- https://svgartista.net/ (use this for the `keySplines` information)