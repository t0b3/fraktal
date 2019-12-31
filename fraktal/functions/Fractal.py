import numpy as np
from PIL import Image

# abstract class: DO NOT USE! - use child classes instead
class Fractal(object):
    def __init__(self):
        self.iterate_max = 100

    # return an image based on min-max coordinates, size, iterations, palette
    def render_image(self, xmin: float, xmax: float, ymin: float, ymax: float, width: int, height: int,
                     iterate_max: int, palette: list) -> Image.Image:
        # create matrix containing complex plane values
        real = np.linspace(xmin, xmax, num=width, endpoint=False, dtype=np.float64)
        imag = np.linspace(ymax, ymin, num=height, endpoint=False, dtype=np.float64) * 1j
        C = np.ravel(real + imag[:, np.newaxis]).astype(np.complex128)
        # calc mandelbrot set
        import time
        start_main = time.time()
        T = self.calc_fractal(C, {"iterate_max": iterate_max})
        end_main = time.time()
        secs = end_main - start_main
        print(secs)
        # convert values to image
        image: Image.Image = Image.fromarray(T.reshape(height, width).astype('uint8'), mode="P")
        image.putpalette(palette)
        return image

    def get_parameters(self) -> dict:
        return {
            "iterate_max": self.iterate_max,
        }

    def __read_params__(self, params: dict):
        try:
            for key, value in params.items():
                setattr(self, key, value)
        except TypeError as err:
            print(err)
            raise Exception(str(key) + " has the wrong type!")


class Mandelbrot(Fractal):

    # return mandelbrot set i.e. depth values as matrix
    '''opencl implementation'''
    def calc_fractal_opencl(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        import pyopencl as cl

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
    def calc_fractal_numpy(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

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

class Julia(Fractal):
    def __init__(self, c = -0.8+0.155j):
        super().__init__()
        self.c = c

    # return julia set i.e. depth values as matrix
    '''opencl implementation'''

    def calc_fractal_opencl(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        import pyopencl as cl

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
    def calc_fractal_numpy(self, Z: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

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


class Mandelbrot4(Fractal):
    # return mandelbrot set i.e. depth values as matrix
    '''opencl implementation'''

    def calc_fractal_opencl(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        import pyopencl as cl

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

    def calc_fractal_numpy(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

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


class Julia4(Fractal):
    def __init__(self, c=-0.8 + 0.155j):
        super().__init__()
        self.c = c

    # return julia set i.e. depth values as matrix
    '''opencl implementation'''

    def calc_fractal_opencl(self, q: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

        import pyopencl as cl

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

    def calc_fractal_numpy(self, Z: np.ndarray, param: dict) -> np.ndarray:
        self.__read_params__(param)

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

    def get_parameters(self) -> dict:
        d = super().get_parameters()
        d["c"] = self.c
        return d
