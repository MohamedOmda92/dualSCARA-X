/* Include files */

#include "SCARA_Control_System_cgxe.h"
#include "m_nM5NMYJUCkhQa81HtyaWRC.h"

unsigned int cgxe_SCARA_Control_System_method_dispatcher(SimStruct* S, int_T
  method, void* data)
{
  if (ssGetChecksum0(S) == 379544242 &&
      ssGetChecksum1(S) == 1857591515 &&
      ssGetChecksum2(S) == 2217442561 &&
      ssGetChecksum3(S) == 2882170488) {
    method_dispatcher_nM5NMYJUCkhQa81HtyaWRC(S, method, data);
    return 1;
  }

  return 0;
}
