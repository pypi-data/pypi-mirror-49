#ifndef __FPGA_HPP_
#define __FPGA_HPP_

#include <vector>
#include <stdexcept>
#include <cassert>

#include <unistd.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#if !defined(_WIN32)
#include <poll.h>
#endif
#include <sys/types.h>
#include <sys/stat.h>

#include "tensorflow/core/platform/mutex.h"
#include "tensorflow/core/platform/logging.h"

#define PRINT_DEBUG_INFO TF_PREDICT_FALSE(VLOG_IS_ON(1))

#define EPU_NUM          2

#define EPU_MEM_BASE     0x200000000
#define EPU0_MEM_BASE    0x201000000
#define EPU0_MEM_SIZE    0x0FF000000
#define EPU1_MEM_BASE    0x301000000
#define EPU1_MEM_SIZE    0x0FF000000

#define EPU0_REG_BASE    0x00200000
#define EPU1_REG_BASE    0x00300000

#define EVENT_CHANNEL    4

using namespace std;


class FPGA {
public:
    FPGA(void);
    ~FPGA(void);

    void reg_write(off_t target, uint32_t writeval);

    uint32_t reg_read(off_t target);

    char evt_read(int index, int timeout);

    // Memcpy H2D & D2H
    void memcpyH2D(void* dest, const void* source, size_t count);

    void memcpyD2H(void* dest, const void* source, size_t count);

private:
    string get_file_content(string path);
    bool find_epu_path(string vendor_id, string device_id, string& found_path);
    int file_open(const string& file_name);
    int mmap_open(const string& file_name, void **base, uint32_t size);
    void file_close(int fd);
    void mmap_close(int fd, void *base, uint32_t size);

    mutable tensorflow::mutex H2D_mu_;
    mutable tensorflow::mutex D2H_mu_;

    void* _mem_base;
    void* _reg_base;
    void* _iatu_base;
    int _mem_fd;
    int _reg_fd;
    int _iatu_fd;
    int _ctrl_fd;
    int _conf_fd;
    int _evt_fd[EVENT_CHANNEL] = {-1};
#if !defined(_WIN32)
    //struct pollfd fds[EVENT_CHANNEL][1];
#endif
};

#endif // __FPGA_HPP_
