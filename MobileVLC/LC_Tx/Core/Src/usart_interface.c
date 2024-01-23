#include "usart_interface.h"
#include "string.h"

uint8_t buffer_TX1[TX1_Size];
uint8_t buffer_RX1[RX1_Size];
uint16_t Rx1_Count=0;					//接收数据计数

///重定向c库函数printf到串口，重定向后可使用printf函数
#ifdef __GNUC__
#define PUTCHAR_PROTOTYPE int __io_putchar(int ch)
#else
#define PUTCHAR_PROTOTYPE int fputc(int ch, FILE *f)
#endif

///选择使用printf串口发送数据的类型
#define HAL_USART							///<HAL普通串口发送数据
//#define HAL_USART_DMA				///<HAL DMA 串口发送数据
PUTCHAR_PROTOTYPE{
	#ifdef HAL_USART
		HAL_UART_Transmit(&huart1, (uint8_t *)&ch, 1, 0xffff);	///<普通串口发送数据
	#endif

	#ifdef HAL_USART_DMA
		HAL_UART_Transmit_DMA(&huart1,(uint8_t *)&ch,1);		///<DMA串口发送数据
	#endif
	    return ch;
}

void usartSend(void* dateAdr,	uint16_t size){
	size=size>TX1_Size	?	TX1_Size	:	size;
	memcpy(buffer_TX1,dateAdr,(size>TX1_Size?TX1_Size:size));			//复制发送数据到发送数组的内存
	HAL_UART_Transmit_DMA(&huart1,buffer_TX1,size);
}

//stm32f4xx_it.c里面void USART2_IRQHandler(void);中加入该函数调用放在清除中断标志函数之上
void USART_IRQHandler_myself(UART_HandleTypeDef *huart){			//接收完成中断函数
	if(__HAL_UART_GET_FLAG(huart,UART_FLAG_IDLE)!=RESET){			//帧接收中断（空闲中断)
				__HAL_UART_CLEAR_IDLEFLAG(huart);
				HAL_UART_DMAStop(huart);														//关闭DMA，防止处理期间有数据
				if(huart->Instance==USART1){
					Rx1_Count=RX1_Size-hdma_usart1_rx.Instance->CNDTR;			//接收数据个数
					/*********************************start接收完成处理代码************************/
					usartSend(buffer_RX1,Rx1_Count);
					/***********************************end****************************************/
					HAL_UART_Receive_DMA(huart,buffer_RX1,RX1_Size);			//开启DMA继续接受数据
				}
	}
}
