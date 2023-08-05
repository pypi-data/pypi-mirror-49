#ifndef TENSORFLOW_COMMON_RUNTIME_FPGA_FPGA_DEVICE_FACTORY_H_
#define TENSORFLOW_COMMON_RUNTIME_FPGA_FPGA_DEVICE_FACTORY_H_

// Register a factory that provides FPGA devices.
#include "tensorflow/core/common_runtime/fpga/fpga_device.h"

#include <vector>
#include "tensorflow/core/common_runtime/device_factory.h"
#include "tensorflow/core/framework/allocator.h"
#include "tensorflow/core/public/session_options.h"

namespace tensorflow {

class FPGADeviceFactory : public DeviceFactory {
 public:
  Status CreateDevices(const SessionOptions& options, const string& name_prefix,
                       std::vector<std::unique_ptr<Device>>* devices) override;
  ~FPGADeviceFactory();

 private:
  bool inited = false;
  FPGA* fpga;
  FPGAAllocator* fa[EPU_NUM];
  FPGADeviceContextCoreX* ctx[EPU_NUM];
  VirtexDNN* dnn[EPU_NUM];
  string name[EPU_NUM];
};

}  // namespace tensorflow
#endif
