# flashloan

aave： 只要追踪flashloan事件即可\
dydx： 四个事件按顺序即可\
uniswap: \
1.找PairCreate中的对合约地址（提供swap函数的）\
         2.在对合约中找触发swap事件的tx\
         3.判断tx：\
            1）调用swap函数时，data是否大于0\
            2）由uniswapV2Call触发的内部事务必须带哦用transfer or transferFrom函数\
            3）transfer，transferFrom函数地址为对合约地址
