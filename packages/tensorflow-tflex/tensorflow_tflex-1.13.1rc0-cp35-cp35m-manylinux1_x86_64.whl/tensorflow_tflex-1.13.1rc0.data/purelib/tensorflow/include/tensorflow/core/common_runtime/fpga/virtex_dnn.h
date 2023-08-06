#ifndef TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_VIRTEX_DNN_H_
#define TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_VIRTEX_DNN_H_

#include "tensorflow/core/common_runtime/fpga/axi_top.h"
#include "tensorflow/core/common_runtime/fpga/fpga.h"
#include "tensorflow/core/platform/mutex.h"


namespace corex {
    /* Memory management */
    enum MemcpyKind {
        // Host -> Host
        MemcpyHostToHost = 0,
        // Host -> Device
        MemcpyHostToDevice = 1,
        // Device -> Host
        MemcpyDeviceToHost = 2,
        // Device -> Device
        MemcpyDeviceToDevice = 3,
        // Direction of the transfer is inferred from the pointer values. Requires unified virtual addressing
        MemcpyDefault = 4,
    };
};


class VirtexDNN {
public:
    VirtexDNN(uint32_t axi_reg_baseaddr, FPGA *fpga);

    virtual void ConvolutionForward(
            const void* input, const void* filter, void* output, const void* bias,
            const void* second_input, int input_rows, int input_cols, int in_depth,
            int filter_rows, int filter_cols, int pad_rows, int pad_cols,
            int out_rows, int out_cols, int out_depth, int stride,
            bool bias_enable, bool second_input_enable, bool relu_enable, bool async);

    virtual void PoolForward(
            const void* input_ptr, void* output_ptr, int in_cols, int in_rows,
            int in_depth, int out_height, int out_width, int ksize, bool async);

    virtual void PadForward(
            const void* input_ptr, void* output_ptr, int input_cols, int input_rows,
            int in_depth, int out_rows, int out_cols, bool cast_enable, bool async);

    void Sync();

private:
    axi_Top epu;

    mutable tensorflow::mutex mu_; 
    enum EPU_REG start_reg = NO_START;
};
#endif // _VIRTEX_DNN_H_
