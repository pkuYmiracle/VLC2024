# Hardware

硬件代码详解。

## Sender(LC_Tx)

```cpp
while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,0);
    if(USART1_RECV_CPLT_FLAG ==1)
    {
        for(int i=0;i<32;++i)
        {
            HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,4095);
            HAL_Delay(10);
        }
        for(int i=0;i<16;++i)
        {
            HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,0);
            HAL_Delay(10);
        }
        for(int i=0;i<8;i++)
        {
            uint8_t bit_val=(USART1_RX_LEN>>(7-j))&1;
            HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,2500);
            HAL_Delay(10);
            HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,bit_val*4095);
            HAL_Delay(10);
        }
        for(int i=0;i<USART1_RX_LEN;i++)
        {
            uint8_t val=USART1_RX_BUF[i];
            for(uint8_t j=0;j<8;++j)
            {
                uint8_t bit_val=(val>>(7-j))&1;
                HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,2500);
                HAL_Delay(10);
                HAL_DAC_SetValue(&hdac1,DAC_CHANNEL_2,DAC_ALIGN_12B_R,bit_val*4095);
                HAL_Delay(10);
            }
        }
        printf("Transmission Over.\n");
        // 清除数据
        memset(USART1_RX_BUF,0,USART1_RX_BUF_SIZE);
        USART1_RX_LEN=0;//清除计数
        USART1_RECV_CPLT_FLAG=0;//清除接收结束标志位
    }
    HAL_UART_Receive_DMA(&huart1,USART1_RX_BUF,USART1_RX_BUF_SIZE);
  }
  /* USER CODE END 3 */
```

Sender 端，我用 USART DMA 从主机向 MCU 传递数据。
每当完成一次传输后，MCU 将通过 DAC 设置液晶所连引脚上的电压。
间隔法：
物理层的编码工作在sender端的MCU完成。

1. 从串口接收到一串16进制串后，传输开始。
2. MCU将连续将液晶设置成高电压，以表示传输开始，然后，输出固定长度的低电压，以方便接受端定位有效数据的开始。
3. 将16进制串的长度转译为01串，遍历01串的每一位。先设置引脚DAC为2500，作为间隔符用以回复时钟。等待10ms后，查看01串该位的值，若为0，则设置引脚DAC为0，若为1，则设置引脚DAC为4095。再等待10ms。
4. 之后，将得到的16进制串转译为01串，遍历01串的每一位，做3中一样的事。

其他编码：尚未完成。

## Receiver(Test_eval)

```cpp
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if(htim->Instance==TIM3)
    {
        HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
        value_adc = HAL_ADC_GetValue(&hadc1);
        HAL_UART_Transmit_DMA(&huart1,(uint8_t*)&value_adc,sizeof(uint32_t));
    }
}
```

Receiver 的执行逻辑不在main函数中，而在Timer的callback中。
每间隔一段时间（譬如 1ms），就调用一次 HAL_TIM_PeriodElapsedCallback。
HAL_TIM_PeriodElapsedCallback：

1. 通过 ADC Poll 得到该时刻光敏传感器（具体叫什么我也不太清楚）的值。
2. 通过 DMA 将此值通过串口传输回主机。
