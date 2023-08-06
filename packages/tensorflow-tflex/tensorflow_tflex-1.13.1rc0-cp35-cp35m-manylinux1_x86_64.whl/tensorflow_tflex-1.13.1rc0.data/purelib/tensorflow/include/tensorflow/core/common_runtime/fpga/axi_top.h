#ifndef TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_AXI_TOP_H_
#define TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_AXI_TOP_H_

#include <unistd.h>
#include <iostream> 
#include <cmath> 
#include <chrono>
#include "tensorflow/core/platform/mutex.h"
#include "tensorflow/core/common_runtime/fpga/fpga.h"


#define CEIL(x, y)   ((x + y - 1) / y)
#define FLOOR(x, y)  (x / y)

#define AXI_REG_STEP      4

#define NO_START          (enum EPU_REG)0
#define CONV_START        PARAM_START_REG
#define MP_START          MP_START_REG

/* EPU register offset */
enum EPU_REG {
    /* convolution register offset */
    PARAM_CH_REG = (uint32_t)0,
    PARAM_CW_REG,
    PARAM_CC_REG,
    PARAM_CK_REG,
    PARAM_CR_REG,
    PARAM_CS_REG,
    PARAM_LH_REG,
    PARAM_LW_REG,
    PARAM_STRIDE_REG,
    PARAM_PAD_REG,
    PARAM_RELU_EN_REG,
    PARAM_INPUT_SIZE_L_REG,
    PARAM_INPUT_SIZE_H_REG,
    PARAM_WEIGHT_SIZE_L_REG,
    PARAM_WEIGHT_SIZE_H_REG,
    PARAM_CH_PRIME_REG,
    PARAM_CW_PRIME_REG,
    PARAM_LH_PRIME_REG,
    PARAM_LW_PRIME_REG,
    PARAM_H_STEP_REG,
    PARAM_W_STEP_REG,
    PARAM_CHLH_PRIME_REG,
    PARAM_CWLW_PRIME_REG,
    PARAM_CKLN_REG,
    PARAM_CCLM_REG,
    PARAM_CRCS_REG,
    PARAM_CHCW_REG,
    PARAM_LHLW_REG,
    PARAM_DDR_IA_REG,
    PARAM_DDR_WT_REG,
    PARAM_DDR_SS_REG,
    PARAM_DDR_BS_REG,
    PARAM_DDR_OA_REG,
    PARAM_START_REG,
    PARAM_SS_EN_REG,
    PARAM_BS_EN_REG,
    ID_IA_REG,
    ID_WT_REG,
    ID_SS_REG,
    ID_BS_REG,
    /* maxpool register offset */
    MP_START_REG = (uint32_t)0x1e8 >> 2,
    CHANNEL_REG,
    IA_BASE_REG,
    IA_W_REG,
    IA_SIZE_REG,
    OA_BASE_REG,
    OA_W_REG,
    OA_SIZE_REG,
    MP_MODE_REG,
    MP_DONE_SIG_REG,
    MP_DONE_CLR_REG,
    MP_DEBUG_CONFIG_REG,
    MP_DEBUG_STATUS_REG,
    ID_MP_REG
};


class axi_Top {
public:
    axi_Top(const uint32_t axi_reg_baseaddr, FPGA *fpga);

    /* inference sequence: start -> wait until done */
    void clear(uint32_t start_reg_offset);
    void reset(uint32_t start_reg_offset);
    void start_inference(uint32_t start_reg_offset);
    void wait_until_done(uint32_t start_reg_offset);

    void pad_exec(
        const void* input_ptr, void* output_ptr, int input_cols, int input_rows,
        int in_depth, int out_rows, int out_cols, bool cast_enable);
    void pool_exec(
        const void* input_ptr, void* output_ptr, int in_cols, int in_rows,
        int in_depth, int out_height, int out_width, int ksize);
    void conv_exec(
        const void* input, const void* filter, void* output, const void* bias,
        const void* second_input, int input_rows, int input_cols, int in_depth,
        int filter_rows, int filter_cols, int pad_rows, int pad_cols,
        int out_rows, int out_cols, int out_depth, int stride,
        bool bias_enable, bool second_input_enable, bool relu_enable);

private:
    /* register read */
    uint32_t read_reg_u32(uint32_t offset) const;
    /* register write */
    void write_reg_u32(uint32_t offset, uint32_t value) const;

    void get_h_w(uint32_t* h, uint32_t* w, uint32_t H, uint32_t W, uint32_t R, uint32_t stride, uint32_t si_en);

    /* fpga instance  */
    FPGA *fpga_;
    /* register base address */
    uint32_t axi_reg_baseaddr;
    /* time to profiling */
    std::chrono::time_point<std::chrono::steady_clock> start_time, start_time2, end_time;
};

#endif
