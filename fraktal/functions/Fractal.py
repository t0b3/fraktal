import pyopencl as cl
import numpy as np

class Mandelbrot(object):
    def __init__(self, iterate_max: int = 100, *unused_args, **kwargs):
        self.iterate_max = iterate_max

    def get_parameters(self) -> dict:
        return {
            "iterate_max": self.iterate_max,
        }


    # return mandelbrot set i.e. depth values as matrix
    '''opencl implementation'''
    def calc_fractal_opencl(self, q: np.ndarray) -> np.ndarray:
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        output = np.empty(q.shape, dtype=np.uint32)
        mf = cl.mem_flags
        q_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=q)
        output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

        prg = cl.Program(ctx, """//CL//
        #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
        #pragma OPENCL EXTENSION cl_khr_fp64 : enable
        __kernel void mandelbrot(__global double2 *q,
                         __global uint *output, uint const maxiter)
        {
            int gid = get_global_id(0);
            double nreal, real = 0;
            double imag = 0;
        
            output[gid] = maxiter-1;
        
            for(int curiter = 0; curiter < maxiter; curiter++) {
                nreal = real*real - imag*imag + q[gid].x;
                imag = 2* real*imag + q[gid].y;
                real = nreal;
        
                if (real*real + imag*imag >= 4.0f) {
                     output[gid] = curiter;
                     break;
                }
            }
          
        }
        """).build()

        prg.mandelbrot(queue, output.shape, None, q_opencl,
                       output_opencl, np.uint32(self.iterate_max))
        cl.enqueue_copy(queue, output, output_opencl).wait()
        return output

    # return mandelbrot set i.e. depth values as matrix
    '''numpy implementation'''
    def calc_fractal_numpy(self, q: np.ndarray) -> np.ndarray:
        # init helper matrices
        Z = np.zeros_like(q, np.complex128)
        T = np.zeros(q.shape, np.uint32)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 2 + q[M]
            T[M] = k
        return T

    #calc_fractal = calc_fractal_numpy
    calc_fractal = calc_fractal_opencl

class Julia(Mandelbrot):
    def __init__(self, iterate_max: int = 100, c: complex = -0.8+0.155j):
        super().__init__(iterate_max)
        self.c = c

    # return julia set i.e. depth values as matrix
    '''opencl implementation'''
    def calc_fractal_opencl(self, q: np.ndarray) -> np.ndarray:
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        output = np.empty(q.shape, dtype=np.uint32)
        mf = cl.mem_flags
        q_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=q)
        output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

        prg = cl.Program(ctx, """//CL//
        #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
        #pragma OPENCL EXTENSION cl_khr_fp64 : enable
        __kernel void julia(__global double2 *q,
                         __global uint *output, uint const maxiter, double2 const c)
        {
            int gid = get_global_id(0);
            double nreal, real = q[gid].x;
            double imag = q[gid].y;

            output[gid] = maxiter-1;

            for(int curiter = 0; curiter < maxiter; curiter++) {
                nreal = real*real - imag*imag + c.x;
                imag = 2* real*imag + c.y;
                real = nreal;

                if (real*real + imag*imag >= 4.0f) {
                     output[gid] = curiter;
                     break;
                }
            }

        }
        """).build()

        prg.julia(queue, output.shape, None, q_opencl,
                  output_opencl, np.uint32(self.iterate_max), np.complex128(self.c))
        cl.enqueue_copy(queue, output, output_opencl).wait()
        return output

    # return julia set i.e. depth values as matrix
    '''numpy implementation'''
    def calc_fractal_numpy(self, Z: np.ndarray) -> np.ndarray:
        # init helper matrices
        T = np.zeros(Z.shape, np.uint32)
        c = np.complex128(self.c)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 2 + c
            T[M] = k
        return T

    #calc_fractal = calc_fractal_numpy
    calc_fractal = calc_fractal_opencl

    def get_parameters(self) -> dict:
        d = super().get_parameters()
        d["c"] = self.c
        return d


class Mandelbrot4(Mandelbrot):
    # return mandelbrot set i.e. depth values as matrix
    '''opencl implementation'''
    def calc_fractal_opencl(self, q: np.ndarray) -> np.ndarray:
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        output = np.empty(q.shape, dtype=np.uint32)
        mf = cl.mem_flags
        q_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=q)
        output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

        prg = cl.Program(ctx, """//CL//
        #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
        #pragma OPENCL EXTENSION cl_khr_fp64 : enable
        __kernel void mandelbrot(__global double2 *q,
                         __global uint *output, uint const maxiter)
        {
            int gid = get_global_id(0);
            double nreal, real = 0;
            double imag = 0;

            output[gid] = maxiter-1;

            for(int curiter = 0; curiter < maxiter; curiter++) {
                nreal = real*real - imag*imag;
                imag = 2* real*imag;
                real = nreal;
                nreal = real*real - imag*imag + q[gid].x;
                imag = 2* real*imag + q[gid].y;
                real = nreal;

                if (real*real + imag*imag >= 4.0f) {
                     output[gid] = curiter;
                     break;
                }
            }

        }
        """).build()

        prg.mandelbrot(queue, output.shape, None, q_opencl,
                       output_opencl, np.uint32(self.iterate_max))
        cl.enqueue_copy(queue, output, output_opencl).wait()
        return output

    # return mandelbrot set i.e. depth values as matrix
    '''numpy implementation'''

    def calc_fractal_numpy(self, q: np.ndarray) -> np.ndarray:
        # init helper matrices
        Z = np.zeros_like(q, np.complex128)
        T = np.zeros(q.shape, np.uint32)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 4 + q[M]
            T[M] = k
        return T

    # calc_fractal = calc_fractal_numpy
    calc_fractal = calc_fractal_opencl


class Julia4(Julia):
    # return julia set i.e. depth values as matrix
    '''opencl implementation'''
    def calc_fractal_opencl(self, q: np.ndarray) -> np.ndarray:
        ctx = cl.create_some_context()
        queue = cl.CommandQueue(ctx)
        output = np.empty(q.shape, dtype=np.uint32)
        mf = cl.mem_flags
        q_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=q)
        output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

        prg = cl.Program(ctx, """//CL//
        #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
        #pragma OPENCL EXTENSION cl_khr_fp64 : enable
        __kernel void julia(__global double2 *q,
                         __global uint *output, uint const maxiter, double2 const c)
        {
            int gid = get_global_id(0);
            double nreal, real = q[gid].x;
            double imag = q[gid].y;

            output[gid] = maxiter-1;

            for(int curiter = 0; curiter < maxiter; curiter++) {
                nreal = real*real - imag*imag;
                imag = 2* real*imag;
                real = nreal;
                nreal = real*real - imag*imag + c.x;
                imag = 2* real*imag + c.y;
                real = nreal;

                if (real*real + imag*imag >= 4.0f) {
                     output[gid] = curiter;
                     break;
                }
            }

        }
        """).build()

        prg.julia(queue, output.shape, None, q_opencl,
                  output_opencl, np.uint32(self.iterate_max), np.complex128(self.c))
        cl.enqueue_copy(queue, output, output_opencl).wait()
        return output

    # return julia set i.e. depth values as matrix
    '''numpy implementation'''
    def calc_fractal_numpy(self, Z: np.ndarray) -> np.ndarray:
        # init helper matrices
        T = np.zeros(Z.shape, np.uint32)
        c = np.complex128(self.c)
        # calculate fractal image values
        for k in range(self.iterate_max):
            M = abs(Z) < 2
            Z[M] = Z[M] ** 4 + c
            T[M] = k
        return T

    # calc_fractal = calc_fractal_numpy
    calc_fractal = calc_fractal_opencl



formulas = {"mandelbrot": Mandelbrot,
           "julia": Julia,
           "mandelbrot4": Mandelbrot4,
           "julia4": Julia4}