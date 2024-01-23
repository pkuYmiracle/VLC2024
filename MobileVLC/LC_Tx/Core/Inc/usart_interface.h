#include "stm32g0xx.h"
#include "stdio.h"

#define	TX1_Size		500								//定义串口发送接收缓存大小
#define	RX1_Size		500

extern UART_HandleTypeDef huart1;			//在配置生成的usart.c文件里的结构体
extern DMA_HandleTypeDef hdma_usart1_rx;
extern DMA_HandleTypeDef hdma_usart1_tx;

//调试串口
extern uint8_t buffer_TX1[TX1_Size];
extern uint8_t buffer_RX1[RX1_Size];
extern uint16_t Rx1_Count1;

//发送数据函数
void usartSend(void* dateAdr,uint16_t size);
