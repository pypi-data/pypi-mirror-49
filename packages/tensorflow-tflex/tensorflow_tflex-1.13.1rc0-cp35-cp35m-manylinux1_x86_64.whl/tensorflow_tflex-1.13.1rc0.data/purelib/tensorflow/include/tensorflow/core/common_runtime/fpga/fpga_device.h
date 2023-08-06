#ifndef TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_FPGA_DEVICE_H_
#define TENSORFLOW_CORE_COMMON_RUNTIME_FPGA_FPGA_DEVICE_H_

#include "tensorflow/core/common_runtime/device_factory.h"
#include "tensorflow/core/common_runtime/local_device.h"
#include "tensorflow/core/common_runtime/fpga/fpga_device_context.h"
#include "tensorflow/core/common_runtime/fpga/fpga_allocator.h"
#include "tensorflow/core/common_runtime/fpga/fpga.h"
#include "tensorflow/core/common_runtime/fpga/virtex_dnn.h"

namespace tensorflow {

// CPU device implementation.
class FPGADevice : public LocalDevice {
 public:
  FPGADevice(const SessionOptions& options, const string& name,
                   Bytes memory_limit, const DeviceLocality& locality,
                   Allocator* allocator,
                   FPGAAllocator* fpga_allocator,
                   FPGADeviceContext* ctx,
                   string description,
                   FPGA *fpga, 
                   VirtexDNN *dnn);
  ~FPGADevice() override;

  void Compute(OpKernel* op_kernel, OpKernelContext* context) override;
  Allocator* GetAllocator(AllocatorAttributes attr) override;
  Status FillContextMap(const Graph *graph, DeviceContextMap *device_context_map) override; 
  Status MakeTensorFromProto(const TensorProto& tensor_proto,
                             const AllocatorAttributes alloc_attrs,
                             Tensor* tensor) override;

  Status Sync() override { 
    // for now, assuming only one VirtexDNN and one FPGA
    // in one FPGADevice
    VLOG(0) << "\33[43mFPGA_DEVICE Sync()\33[0m";    
    get_dnn()->Sync();
    VLOG(0) << "\33[43mFPGA_DEVICE Sync Done()\33[0m";    
    return Status::OK(); 
  }
   
  void memcpyH2D(void *dst, const void *src, size_t count); 
  void memcpyD2H(void *dst, const void *src, size_t count);

  VirtexDNN *get_dnn() {
    return dnn_;
  }

  FPGAAllocator *get_fpga_allocator() {
    return fpga_allocator_;
  }

 private:
  FPGA *fpga_;                         // not owned
  VirtexDNN *dnn_;                     // not owned
  Allocator* allocator_;               // Not owned
  FPGAAllocator* fpga_allocator_;      // not owned
  FPGADeviceContext* device_context_;  // not owned

  void memcpy(void* dst, const void* src, size_t count, ::corex::MemcpyKind kind);
};

}  // namespace tensorflow

#endif  // TENSORFLOW_CORE_COMMON_RUNTIME_THREADPOOL_DEVICE_H_
