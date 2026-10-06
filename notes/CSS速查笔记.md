# CSS 速查笔记

## 怎么用这份文件

这份笔记讲 **CSS（网页样式）**：怎么写、怎么选中元素、页面结构怎么看。忘了哪条，看下面索引表点名字跳过去。每条固定三段：**解析**（白话讲概念）／**操作**（能照抄的例子）／`> ⚠️` 坑。标题末尾带 🔒 的是安全相关条目。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| 一 引入方式 | [`引入 CSS 的三种方式`](#引入-css-的三种方式-总览先看这一条) | 总览先看这一条 |
| 一 引入方式 | [`style 标签`](#style-标签-在-html-里直接写样式) | 在 HTML 里直接写样式 |
| 一 引入方式 | [`外部样式表 link`](#外部样式表-link-单独一个-css-文件) | 单独一个 css 文件 |
| 一 引入方式 | [`行内 style 属性`](#行内-style-属性-在标签上直接写) | 在标签上直接写 |
| 二 选择器 | [`元素选择器`](#元素选择器-按标签名选) | 按标签名选 |
| 二 选择器 | [`类选择器 .x`](#类选择器-x-按-class-选最常用) | 按 class 选最常用 |
| 二 选择器 | [`ID 选择器 #x`](#id-选择器-x-按-id-选唯一的那个) | 按 id 选唯一的那个 |
| 二 选择器 | [`后代选择器`](#后代选择器-空格表示包含关系) | 空格表示包含关系 |
| 二 选择器 | [`群组选择器`](#群组选择器-逗号一次选多个) | 逗号一次选多个 |
| 二 选择器 | [`伪类选择器 :hover`](#伪类选择器-hover-鼠标悬停时生效) | 鼠标悬停时生效 |
| 三 常用属性 | [`color`](#color-文字颜色) | 文字颜色 |
| 三 常用属性 | [`background`](#background-背景颜色与图片) | 背景颜色与图片 |
| 三 常用属性 | [`font-size`](#font-size-字号) | 字号 |
| 三 常用属性 | [`margin 与 padding`](#margin-与-padding-外边距与内边距) | 外边距与内边距 |
| 三 常用属性 | [`border`](#border-边框) | 边框 |
| 三 常用属性 | [`width 与 height`](#width-与-height-宽和高) | 宽和高 |
| 三 常用属性 | [`display`](#display-块级行内怎么排) | 块级行内怎么排 |
| 三 常用属性 | [`position`](#position-定位脱离正常流) | 定位脱离正常流 |
| 四 盒子模型与布局 | [`盒子模型`](#盒子模型-内容内边距边框外边距) | 内容内边距边框外边距 |
| 四 盒子模型与布局 | [`优先级与层叠`](#优先级与层叠-冲突时谁说了算) | 冲突时谁说了算 |
| 四 盒子模型与布局 | [`flex 简单布局`](#flex-简单布局-让子元素一行排开) | 让子元素一行排开 |
| 五 CSS 与安全 | [`CSS 与 Web 安全的关系`](#css-与-web-安全的关系-排查注入点时顺带看一眼) | 排查注入点时顺带看一眼 |

---


CSS（层叠样式表）决定网页「长什么样」。下篇先讲样式怎么引入，再讲怎么选中元素、常用属性、布局规则，最后说清它和 Web 安全的关系。

## 一 引入方式

### `引入 CSS 的三种方式` 总览先看这一条

**解析**　CSS 负责网页「长什么样」。想让它生效，得先「引入」到 HTML 里，就三种方式：①`<style>` 标签把样式写在页面里；②外部 `.css` 文件用 `<link>` 引进来；③直接在标签上写 `style=""` 属性。实际项目一般用 ②，临时调试用 ③。（三件事的分工：HTML 管「有什么」，CSS 管「长什么样」，JS 管「会动什么」。）

**操作**

```text
方式一（页内）： <style> p { color: red; } </style>
方式二（外部）： <link rel="stylesheet" href="style.css">
方式三（行内）： <p style="color: red;">你好</p>
```

> ⚠️ 坑：三种都在时，行内 `style` 优先级最高（详见「优先级与层叠」）。

### `style 标签` 在 HTML 里直接写样式

**解析**　在 `<head>` 里放一个 `<style>...</style>`，把 CSS 规则写进去，整个页面都能用。适合单页面、小 demo。规则格式固定是 `选择器 { 属性: 值; }`。

**操作**

```text
<!DOCTYPE html>
<html>
<head>
  <style>
    p    { color: blue; font-size: 20px; }
    .hi  { background: yellow; }
  </style>
</head>
<body>
  <p>蓝色文字</p>
  <p class="hi">带黄色背景</p>
</body>
</html>
```

> ⚠️ 坑：`<style>` 应写在 `<head>` 里；写在 `<body>` 里多数浏览器也认，但不规范。

### `外部样式表 link` 单独一个 css 文件

**解析**　把 CSS 单独存成一个 `.css` 文件，用 `<link rel="stylesheet" href="...">` 引进来。好处是一个文件能被多个页面共用，改一处全站生效——真实网站都这么干，这也是渗透时你能直接下载、读到的「前端源码」之一。

**操作**

```text
style.css：
  body  { font-family: sans-serif; background: #f5f5f5; }
  .btn  { color: #fff; background: #007bff; padding: 8px 16px; }

index.html：
  <link rel="stylesheet" href="style.css">
```

> ⚠️ 坑：`href` 是相对路径时以「当前页面」为基准（见 URL 篇的「相对 URL vs 绝对 URL」）；写成 `/style.css` 才是从网站根目录开始。

### `行内 style 属性` 在标签上直接写

**解析**　直接在标签上写 `style="属性:值;"`，只作用于这一个元素。优先级最高，但写多了难维护，一般只用于临时改一下，或让 JS 动态改样式。

**操作**

```text
<p style="color: red; font-size: 24px;">这行是红色的</p>
<div style="width: 200px; height: 100px; background: #eee;"></div>
```

> ⚠️ 坑：想临时在浏览器里试样式，用 F12 改行内 `style` 最直观，而且只改本地、不影响服务器。

## 二 选择器

### `元素选择器` 按标签名选

**解析**　选择器决定「这条样式作用在哪些元素上」。最基础的是元素（标签）选择器：直接写标签名，如 `p`、`div`、`a`，页面上所有该标签都命中。

**操作**

```text
p   { color: gray; }               → 所有 <p> 段落变灰
a   { color: blue; }               → 所有链接变蓝
div { border: 1px solid #ccc; }    → 所有 <div> 加边框
```

> ⚠️ 坑：影响面最大，页面上所有同标签元素都被改；要精确定位就用类选择器或 ID 选择器。

### `类选择器 .x` 按 class 选最常用

**解析**　HTML 标签可以带 `class="类名"`，CSS 里用 `.类名` 选中它们。同一个类可以贴到很多元素上，一个元素也可以有多个类（用空格隔开）。这是实际开发里用得最多的选择器。

**操作**

```text
HTML： <p class="note">备注</p>
       <span class="note big">又大又带备注</span>

CSS：  .note   { color: orange; }        → 上面两个都命中
       .big    { font-size: 28px; }      → 只命中第二个
       p.note  { font-style: italic; }   → 只命中 <p class="note">
```

> ⚠️ 坑：类名区分大小写；`.note` 前面的那个点不能漏，写成 `note { }`（没点）会被当成元素选择器去找 `<note>` 标签。

### `ID 选择器 #x` 按 id 选唯一的那个

**解析**　HTML 标签可以带 `id="..."`，CSS 里用 `#id名` 选中。按规范，一个页面里 id 必须唯一，所以它只应该命中一个元素。优先级比类选择器高。

**操作**

```text
HTML： <div id="header">页头</div>
       <div id="footer">页脚</div>

CSS：  #header { background: #333; color: #fff; }
       #footer { font-size: 12px; }
```

> ⚠️ 坑：同一页面里 id 重复是「非法但浏览器不报错」，很容易埋坑；JS 的 `document.getElementById` 也依赖 id 唯一。

### `后代选择器` 空格表示包含关系

**解析**　两个选择器之间用**空格**隔开，表示「前面的里面包含后面的」。如 `div p` 选中「所有 `<div>` 内部的 `<p>`」，不管嵌套多深。用它来限定范围，避免改到别处的同类元素。

**操作**

```text
div p       → <div> 里任意深度的所有 <p>
#nav a      → id 为 nav 的元素里的所有链接
ul li span  → 列表项里的 span
```

> ⚠️ 坑：空格是「后代」（任意层级）；只想要「直接子元素」要用 `>`，如 `div > p`。这两个效果不同，且区别很容易被忽略。

### `群组选择器` 逗号一次选多个

**解析**　用**逗号**把多个选择器并列，表示「命中其中任意一个就套用同一套样式」。等价于把同一段 CSS 抄几遍，但更简洁。

**操作**

```text
h1, h2, h3   { font-family: sans-serif; }     → 三级标题共用同一字体
.note, .warn { border-left: 4px solid; }      → 两个类共享样式
```

> ⚠️ 坑：逗号两边是**独立**的选择器；`div, .x` 是「所有 div 加上所有 .x」，不是「div 里的 .x」（那是 `div .x`，中间是空格）。

### `伪类选择器 :hover` 鼠标悬停时生效

**解析**　伪类选择器用 `:状态` 描述元素的某种**状态**，不改变选中的元素，只在状态成立时套样式。最常用 `:hover`（鼠标悬停），还有 `:visited`（访问过的链接）、`:focus`（获得焦点）、`:first-child`（第一个子元素）、`:nth-child(n)` 等。

**操作**

```text
a:hover         { color: red; }         → 鼠标移到链接上变红
li:first-child  { font-weight: bold; }  → 列表第一项加粗
input:focus     { border-color: blue; } → 输入框聚焦时变色
```

> ⚠️ 坑：`:hover` 只在能悬停的设备（鼠标）上有效，手机上一般没有 hover；调试时别忘了它不是「永久生效」的。

## 三 常用属性

### `color` 文字颜色

**解析**　设置文字（前景）颜色。值可以写颜色名（`red`）、十六进制（`#ff0000`）、`rgb(255,0,0)`、`rgba(255,0,0,0.5)`（最后一位是透明度）、`hsl(...)`。

**操作**

```text
p     { color: red; }
h1    { color: #3366cc; }
.note { color: rgba(0, 0, 0, 0.6); }   /* 60% 不透明的黑 */
```

> ⚠️ 坑：`color` 改的是**文字**；改背景要用 `background`，别搞混。

### `background` 背景颜色与图片

**解析**　设置元素的背景，可以是纯色（`background-color`）、图片（`background-image: url(...)`）、渐变等，还能调位置、是否重复。

**操作**

```text
body    { background: #f5f5f5; }
.banner { background: url("/img/banner.jpg") no-repeat center; }
.grad   { background: linear-gradient(to right, #fff, #000); }
```

> ⚠️ 坑：`background` 简写会把没写的子属性**重置为默认值**；只想改一样（比如只改背景色）就用具体的 `background-color`。

### `font-size` 字号

**解析**　设置文字大小。常用单位：`px`（像素，绝对）、`em`（相对父元素字号）、`rem`（相对根元素字号）、`%`、`vw`（相对视口宽度）。

**操作**

```text
p      { font-size: 16px; }
h1     { font-size: 2rem; }    /* 若根字号 16px，则等于 32px */
.small { font-size: 0.8em; }
```

> ⚠️ 坑：`em` 会层层相乘（父元素的 `em` 影响子元素），嵌套深了很难算；`rem` 只看根元素，更可控。

### `margin 与 padding` 外边距与内边距

**解析**　两者都制造空间，但位置不同：`margin`（外边距）是「自己和别人之间的距离」，在边框**外面**；`padding`（内边距）是「边框和内容之间的距离」，在边框**里面**。形象记：padding 是墙里的家具与墙之间的空隙，margin 是墙与邻居之间的空地。四个方向可以单独设（`margin-top` 等），也能用简写，简写按「上 右 下 左」顺时针。

**操作**

```text
.box {
  padding: 10px;          /* 四边内边距都 10px */
  padding: 10px 20px;     /* 上下 10px，左右 20px */
  margin: 20px auto;      /* 上下 20px，左右自动 → 水平居中 */
  margin-top: 5px;        /* 只改上边距 */
}
```

> ⚠️ 坑：相邻两个块元素的上下 `margin` 会**塌陷**（取较大的那个，不是相加），而 `padding` 不会；给元素加背景色就能直观看出 padding 在背景里、margin 在背景外。

### `border` 边框

**解析**　给元素加边框。简写顺序一般是 `宽度 样式 颜色`，如 `1px solid #ccc`。样式有 `solid`（实线）、`dashed`（虚线）、`dotted`（点线）等；也可以只改一边，如 `border-bottom`。

**操作**

```text
.box  { border: 1px solid #ccc; }
.card { border-top: 3px solid #007bff; border-radius: 8px; }   /* 带圆角 */
```

> ⚠️ 坑：`border` 的粗细会被算进元素的「实际占位」（见「盒子模型」），加了边框元素会变胖；不想变胖就加 `box-sizing: border-box`。

### `width 与 height` 宽和高

**解析**　设置元素内容区的宽和高。单位常用 `px`、`%`（相对父元素）、`vw`/`vh`（相对视口）。是否包含 padding 和 border，取决于 `box-sizing`。

**操作**

```text
.box  { width: 200px; height: 100px; }
.half { width: 50%; }                    /* 父元素宽度的 50% */
.full { width: 100vw; height: 100vh; }   /* 铺满整个视口 */
```

> ⚠️ 坑：默认 `box-sizing: content-box` 时 `width:200px` 只算内容，再加上 padding/border 会超过 200px；加 `box-sizing: border-box` 让宽度包含 padding 和 border，更好算。

### `display` 块级行内怎么排

**解析**　决定元素怎么「占位排版」。`block`（块级）：独占一行、能设宽高，如 `<div>`、`<p>`。`inline`（行内）：跟文字排一行、设宽高无效，如 `<span>`、`<a>`。`inline-block`：行内排列但能设宽高。`none`：直接不显示、不占位。`flex`：开启弹性布局（见「flex 简单布局」）。

**操作**

```text
div   { display: block; }         /* 默认就独占一行 */
span  { display: inline; }        /* 默认跟文字走 */
.tag  { display: inline-block; width: 80px; }   /* 能设宽高又不断行 */
.hide { display: none; }          /* 从页面消失，不留位置 */
```

> ⚠️ 坑：`display: none` 是「不占位地消失」，`visibility: hidden` 是「占着位置但看不见」；想隐藏又不想布局乱动，用后者。

### `position` 定位脱离正常流

**解析**　控制元素怎么定位。`static`（默认，正常流）、`relative`（相对自己原来的位置偏移，仍占位）、`absolute`（相对最近的「已定位」祖先偏移，脱离正常流）、`fixed`（相对浏览器窗口，滚动时不动）、`sticky`（滚到某个位置后粘住）。常配合 `top/right/bottom/left` 使用。

**操作**

```text
.box    { position: relative; }                      /* 给子元素做定位基准 */
.tag    { position: absolute; top: 0; right: 0; }    /* 贴到父元素右上角 */
.header { position: fixed; top: 0; width: 100%; }    /* 固定在浏览器顶部 */
```

> ⚠️ 坑：`absolute` 是相对「最近的、position 不是 static 的祖先」定位；如果祖先都没设 position，它会一路找到 `<html>`，结果飞到整页角落——记得给父元素加 `position: relative`。

## 四 盒子模型与布局

### `盒子模型` 内容内边距边框外边距

**解析**　CSS 里每个元素都是一个矩形「盒子」，从里到外分四层：**内容**（content，文字/图片本身）→ **内边距**（padding）→ **边框**（border）→ **外边距**（margin）。元素的「实际占位」由这四层加起来决定。理解它，是看懂「元素为什么比我想的胖/大」的关键。

**操作**

```text
┌──────────────── margin ────────────────┐
│   ┌──────────── border ────────────┐   │
│   │   ┌──────── padding ────────┐   │   │
│   │   │        content          │   │   │
│   │   └─────────────────────────┘   │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘

width:200px; padding:10px; border:1px   → 实际宽度 = 200 + 10×2 + 1×2 = 222px
```

> ⚠️ 坑：用 F12（开发者工具）的「盒模型」面板能一眼看到这四层数值，排查「元素为什么错位」先看它。

### `优先级与层叠` 冲突时谁说了算

**解析**　同一个元素被多条规则命中、又设了同一个属性时，谁生效由**优先级**（选择器越精确越高）和**书写顺序**决定。粗略排序：行内 `style` > `#id` > `.类`/`:伪类`/`[属性]` > `元素`。同优先级则**后写的赢**（这就是「层叠」）。F12 里被划掉的属性，就是「输了」的。

**操作**

```text
优先级（从高到低）：
  行内 style 属性          例：style="color:red"
  #id 选择器               例：#header
  类 / 伪类 / 属性选择器    例：.note / :hover / [type=text]
  元素 / 伪元素选择器        例：p / ::before

p    { color: blue; }
p    { color: red; }    → 同优先级，后写的赢 → 红色
#x   { color: green; }  → id 优先级更高 → 绿色
```

> ⚠️ 坑：`!important` 能强行提高优先级，但用多了样式会彻底失控，前端圈当它「毒药」；看到它先想办法删掉，而不是再加一个压它。

### `flex 简单布局` 让子元素一行排开

**解析**　给父元素加 `display: flex`，它的**直接子元素**就自动排成一行（横向），不再需要 float。父元素上用 `justify-content` 控制主轴（横向）对齐、`align-items` 控制交叉轴（纵向）对齐；子元素上用 `flex: 1` 均分剩余空间。

**操作**

```text
.row {
  display: flex;                  /* 开启弹性布局 */
  justify-content: space-between; /* 主轴两端对齐 */
  align-items: center;            /* 交叉轴居中 */
  gap: 10px;                      /* 子元素之间留 10px 间隙 */
}
.row .item { flex: 1; }           /* 每个子元素平分宽度 */
```

> ⚠️ 坑：`display: flex` 只作用于**直接子元素**，孙元素不受影响；「主轴/交叉轴」最容易记反——`justify-content` 管主轴，`align-items` 管交叉轴。

## 五 CSS 与安全

### `CSS 与 Web 安全的关系` 排查注入点时顺带看一眼🔒

**解析**　🔒 对自学渗透的你，有一条重要认知：**CSS 和 Web 安全基本无关**。它只负责「长什么样」，不处理输入输出、不碰数据库，所以不存在 SQL 注入、命令注入这类问题。极罕见的「CSS 注入」只在特定场景（用户输入被原样塞进 `<style>` 或 style 属性里）才可能被用来读数据，实战中极少遇到，初学阶段可以完全不管。那为什么还要学它？因为**看懂页面结构才能高效找注入点**：知道哪个参数、哪个元素对应哪块功能，你才知道从哪下手，也才能用 F12 定位元素、看表单怎么提交、接口怎么调。

**操作**

```text
渗透视角的真实用途：
  1. 用 F12 看表单 <form> 的 action / method  → 请求发去哪、用 GET 还是 POST
  2. 看输入框的 name 属性                     → 参数名到底叫什么
  3. 用选择器在 Elements 面板定位元素          → 快速找到可注入的位置
  4. 读页面里的链接和接口路径                  → 发现更多攻击面

结论：CSS 本身不产生常见漏洞；「CSS 注入」是极冷门场景，别被名字吓到。
```

> ⚠️ 坑：别把时间花在「找 CSS 漏洞」上；把 CSS 当成「看懂页面、定位元素」的辅助工具，主要精力放在 URL 参数、表单和请求头上。
