(self.webpackChunkttgtcanvas2=self.webpackChunkttgtcanvas2||[]).push([[404],{729:e=>{"use strict";var t=Object.prototype.hasOwnProperty,r="~";function n(){}function i(e,t,r){this.fn=e,this.context=t,this.once=r||!1}function o(e,t,n,o,s){if("function"!=typeof n)throw new TypeError("The listener must be a function");var u=new i(n,o||e,s),a=r?r+t:t;return e._events[a]?e._events[a].fn?e._events[a]=[e._events[a],u]:e._events[a].push(u):(e._events[a]=u,e._eventsCount++),e}function s(e,t){0==--e._eventsCount?e._events=new n:delete e._events[t]}function u(){this._events=new n,this._eventsCount=0}Object.create&&(n.prototype=Object.create(null),(new n).__proto__||(r=!1)),u.prototype.eventNames=function(){var e,n,i=[];if(0===this._eventsCount)return i;for(n in e=this._events)t.call(e,n)&&i.push(r?n.slice(1):n);return Object.getOwnPropertySymbols?i.concat(Object.getOwnPropertySymbols(e)):i},u.prototype.listeners=function(e){var t=r?r+e:e,n=this._events[t];if(!n)return[];if(n.fn)return[n.fn];for(var i=0,o=n.length,s=new Array(o);i<o;i++)s[i]=n[i].fn;return s},u.prototype.listenerCount=function(e){var t=r?r+e:e,n=this._events[t];return n?n.fn?1:n.length:0},u.prototype.emit=function(e,t,n,i,o,s){var u=r?r+e:e;if(!this._events[u])return!1;var a,l,c=this._events[u],h=arguments.length;if(c.fn){switch(c.once&&this.removeListener(e,c.fn,void 0,!0),h){case 1:return c.fn.call(c.context),!0;case 2:return c.fn.call(c.context,t),!0;case 3:return c.fn.call(c.context,t,n),!0;case 4:return c.fn.call(c.context,t,n,i),!0;case 5:return c.fn.call(c.context,t,n,i,o),!0;case 6:return c.fn.call(c.context,t,n,i,o,s),!0}for(l=1,a=new Array(h-1);l<h;l++)a[l-1]=arguments[l];c.fn.apply(c.context,a)}else{var v,_=c.length;for(l=0;l<_;l++)switch(c[l].once&&this.removeListener(e,c[l].fn,void 0,!0),h){case 1:c[l].fn.call(c[l].context);break;case 2:c[l].fn.call(c[l].context,t);break;case 3:c[l].fn.call(c[l].context,t,n);break;case 4:c[l].fn.call(c[l].context,t,n,i);break;default:if(!a)for(v=1,a=new Array(h-1);v<h;v++)a[v-1]=arguments[v];c[l].fn.apply(c[l].context,a)}}return!0},u.prototype.on=function(e,t,r){return o(this,e,t,r,!1)},u.prototype.once=function(e,t,r){return o(this,e,t,r,!0)},u.prototype.removeListener=function(e,t,n,i){var o=r?r+e:e;if(!this._events[o])return this;if(!t)return s(this,o),this;var u=this._events[o];if(u.fn)u.fn!==t||i&&!u.once||n&&u.context!==n||s(this,o);else{for(var a=0,l=[],c=u.length;a<c;a++)(u[a].fn!==t||i&&!u[a].once||n&&u[a].context!==n)&&l.push(u[a]);l.length?this._events[o]=1===l.length?l[0]:l:s(this,o)}return this},u.prototype.removeAllListeners=function(e){var t;return e?(t=r?r+e:e,this._events[t]&&s(this,t)):(this._events=new n,this._eventsCount=0),this},u.prototype.off=u.prototype.removeListener,u.prototype.addListener=u.prototype.on,u.prefixed=r,u.EventEmitter=u,e.exports=u},404:(e,t,r)=>{"use strict";r.r(t),r.d(t,{default:()=>a});var n=r(729);class i extends Error{constructor(e){super(e),this.name="TimeoutError"}}class o{constructor(){Object.defineProperty(this,"_queue",{enumerable:!0,configurable:!0,writable:!0,value:[]})}enqueue(e,t){var r;const n={priority:(t={priority:0,...t}).priority,run:e};if(this.size&&(null===(r=this._queue[this.size-1])||void 0===r?void 0:r.priority)>=t.priority)return void this._queue.push(n);const i=function(e,t,r){let n=0,i=e.length;for(;i>0;){const r=Math.trunc(i/2);let s=n+r;o=e[s],t.priority-o.priority<=0?(n=++s,i-=r+1):i=r}var o;return n}(this._queue,n);this._queue.splice(i,0,n)}dequeue(){const e=this._queue.shift();return null==e?void 0:e.run}filter(e){return this._queue.filter((t=>t.priority===e.priority)).map((e=>e.run))}get size(){return this._queue.length}}const s=()=>{},u=new i;class a extends n{constructor(e){var t,r,n,i;if(super(),Object.defineProperty(this,"_carryoverConcurrencyCount",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_isIntervalIgnored",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_intervalCount",{enumerable:!0,configurable:!0,writable:!0,value:0}),Object.defineProperty(this,"_intervalCap",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_interval",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_intervalEnd",{enumerable:!0,configurable:!0,writable:!0,value:0}),Object.defineProperty(this,"_intervalId",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_timeoutId",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_queue",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_queueClass",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_pendingCount",{enumerable:!0,configurable:!0,writable:!0,value:0}),Object.defineProperty(this,"_concurrency",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_isPaused",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_resolveEmpty",{enumerable:!0,configurable:!0,writable:!0,value:s}),Object.defineProperty(this,"_resolveIdle",{enumerable:!0,configurable:!0,writable:!0,value:s}),Object.defineProperty(this,"_timeout",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),Object.defineProperty(this,"_throwOnTimeout",{enumerable:!0,configurable:!0,writable:!0,value:void 0}),!("number"==typeof(e={carryoverConcurrencyCount:!1,intervalCap:Number.POSITIVE_INFINITY,interval:0,concurrency:Number.POSITIVE_INFINITY,autoStart:!0,queueClass:o,...e}).intervalCap&&e.intervalCap>=1))throw new TypeError(`Expected \`intervalCap\` to be a number from 1 and up, got \`${null!==(r=null===(t=e.intervalCap)||void 0===t?void 0:t.toString())&&void 0!==r?r:""}\` (${typeof e.intervalCap})`);if(void 0===e.interval||!(Number.isFinite(e.interval)&&e.interval>=0))throw new TypeError(`Expected \`interval\` to be a finite number >= 0, got \`${null!==(i=null===(n=e.interval)||void 0===n?void 0:n.toString())&&void 0!==i?i:""}\` (${typeof e.interval})`);this._carryoverConcurrencyCount=e.carryoverConcurrencyCount,this._isIntervalIgnored=e.intervalCap===Number.POSITIVE_INFINITY||0===e.interval,this._intervalCap=e.intervalCap,this._interval=e.interval,this._queue=new e.queueClass,this._queueClass=e.queueClass,this.concurrency=e.concurrency,this._timeout=e.timeout,this._throwOnTimeout=!0===e.throwOnTimeout,this._isPaused=!1===e.autoStart}get _doesIntervalAllowAnother(){return this._isIntervalIgnored||this._intervalCount<this._intervalCap}get _doesConcurrentAllowAnother(){return this._pendingCount<this._concurrency}_next(){this._pendingCount--,this._tryToStartAnother(),this.emit("next")}_resolvePromises(){this._resolveEmpty(),this._resolveEmpty=s,0===this._pendingCount&&(this._resolveIdle(),this._resolveIdle=s,this.emit("idle"))}_onResumeInterval(){this._onInterval(),this._initializeIntervalIfNeeded(),this._timeoutId=void 0}_isIntervalPaused(){const e=Date.now();if(void 0===this._intervalId){const t=this._intervalEnd-e;if(!(t<0))return void 0===this._timeoutId&&(this._timeoutId=setTimeout((()=>{this._onResumeInterval()}),t)),!0;this._intervalCount=this._carryoverConcurrencyCount?this._pendingCount:0}return!1}_tryToStartAnother(){if(0===this._queue.size)return this._intervalId&&clearInterval(this._intervalId),this._intervalId=void 0,this._resolvePromises(),!1;if(!this._isPaused){const e=!this._isIntervalPaused();if(this._doesIntervalAllowAnother&&this._doesConcurrentAllowAnother){const t=this._queue.dequeue();return!!t&&(this.emit("active"),t(),e&&this._initializeIntervalIfNeeded(),!0)}}return!1}_initializeIntervalIfNeeded(){this._isIntervalIgnored||void 0!==this._intervalId||(this._intervalId=setInterval((()=>{this._onInterval()}),this._interval),this._intervalEnd=Date.now()+this._interval)}_onInterval(){0===this._intervalCount&&0===this._pendingCount&&this._intervalId&&(clearInterval(this._intervalId),this._intervalId=void 0),this._intervalCount=this._carryoverConcurrencyCount?this._pendingCount:0,this._processQueue()}_processQueue(){for(;this._tryToStartAnother(););}get concurrency(){return this._concurrency}set concurrency(e){if(!("number"==typeof e&&e>=1))throw new TypeError(`Expected \`concurrency\` to be a number from 1 and up, got \`${e}\` (${typeof e})`);this._concurrency=e,this._processQueue()}async add(e,t={}){return new Promise(((r,n)=>{this._queue.enqueue((async()=>{this._pendingCount++,this._intervalCount++;try{const i=void 0===this._timeout&&void 0===t.timeout?e():function(e,t,r,n){let i;const o=new Promise(((o,s)=>{if("number"!=typeof t||t<0)throw new TypeError("Expected `milliseconds` to be a positive number");t!==Number.POSITIVE_INFINITY?(n={customTimers:{setTimeout,clearTimeout},...n},i=n.customTimers.setTimeout.call(void 0,(()=>{try{o(r())}catch(e){s(e)}}),t),(async()=>{try{o(await e)}catch(e){s(e)}finally{n.customTimers.clearTimeout.call(void 0,i)}})()):o(e)}));return o.clear=()=>{clearTimeout(i),i=void 0},o}(Promise.resolve(e()),void 0===t.timeout?this._timeout:t.timeout,(()=>{(void 0===t.throwOnTimeout?this._throwOnTimeout:t.throwOnTimeout)&&n(u)})),o=await i;r(o),this.emit("completed",o)}catch(e){n(e),this.emit("error",e)}this._next()}),t),this._tryToStartAnother(),this.emit("add")}))}async addAll(e,t){return Promise.all(e.map((async e=>this.add(e,t))))}start(){return this._isPaused?(this._isPaused=!1,this._processQueue(),this):this}pause(){this._isPaused=!0}clear(){this._queue=new this._queueClass}async onEmpty(){if(0!==this._queue.size)return new Promise((e=>{const t=this._resolveEmpty;this._resolveEmpty=()=>{t(),e()}}))}async onSizeLessThan(e){if(!(this._queue.size<e))return new Promise((t=>{const r=()=>{this._queue.size<e&&(this.removeListener("next",r),t())};this.on("next",r)}))}async onIdle(){if(0!==this._pendingCount||0!==this._queue.size)return new Promise((e=>{const t=this._resolveIdle;this._resolveIdle=()=>{t(),e()}}))}get size(){return this._queue.size}sizeBy(e){return this._queue.filter(e).length}get pending(){return this._pendingCount}get isPaused(){return this._isPaused}get timeout(){return this._timeout}set timeout(e){this._timeout=e}}}}]);