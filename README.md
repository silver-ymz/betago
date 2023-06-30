# betago

A simple Go program to play the game of Go.

## run

```bash
rye sync
rye run python src/app.py
```

## dependencies

- [pyside6](https://pypi.org/project/PySide6/): Python bindings for Qt6
- [networkx](https://pypi.org/project/networkx/): Python package for creating and manipulating graphs and networks

## dev-dependencies

- [rye](https://github.com/mitsuhiko/rye): An experimental python project manager, the new project of flask's author

## 说明

本项目是一个简单的围棋程序，使用python编写，使用pyside6作为GUI，使用networkx作为数据结构来简化图论算法代码。
规则方面, 本项目采用了中国围棋规则，即禁止自杀，禁止长打劫，禁止长劫回头打，禁止长打劫回头自杀, 使用比目法判胜负。
超时方面，本项目采用了总时长制，总时长30min，每步时额外加时1min，超时无法继续下棋, 棋权归对手。
本项目在macOS 13上运行良好, windows与linux下未进行测试, 但应该也能正常运行。

### 项目结构

- src: 源代码
  - app.py: 主程序
  - board.py: 棋盘类
  - game.py: 游戏类
  - graph.py: 图论算法
  - window.py: GUI类

### 项目进度

- [x] 基本的围棋规则 (包括自动提子, 禁止自杀, 禁止长打劫, 判断胜负)
- [x] 基本的GUI
- [x] 超时机制

### 项目截图

初始界面
![20230630161714](https://raw.githubusercontent.com/silver-ymz/image/master/20230630161714.png)

结束界面(棋子随意下的)
![20230630161857](https://raw.githubusercontent.com/silver-ymz/image/master/20230630161857.png)