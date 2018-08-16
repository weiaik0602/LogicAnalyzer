#ifndef __USBD_CDC_IF_H__
#define __USBD_CDC_IF_H__

#ifdef __cplusplus
 extern "C" {
#endif
#include <stdint.h>
int htim2;
uint16_t GetCurrentCounterTim2();
uint16_t ReadGpioxIDR(char choose);
uint8_t CDC_Transmit_FS(uint8_t* Buf, uint16_t Len);
void __disable_irq();
void __enable_irq();
/* USER CODE BEGIN EXPORTED_FUNCTIONS */

/* USER CODE END EXPORTED_FUNCTIONS */

/**
  * @}
  */

/**
  * @}
  */

/**
  * @}
  */

#endif /* __USBD_CDC_IF_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
