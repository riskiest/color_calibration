This repo is to implement color adjustment algorithm based on colorchecker.

The main idea of the algorithm is as follows: input a picture with a colorchecker, linearize the input colorchecker colors, and then use the color correction matrix(CCM) to linearly transform the former result to minimize the distance from the standard colorchecker colors. The goal of optimization is the ccm matrix.

After the ccm matrix is calculated, you can enter the picture for correction. The input picture is linearized, then multiplied by the ccm matrix, and then inversely linearized. Note that the rules for linearization and delinearization may be different.

Several linearization mechanisms such as gamma, sgrb, and polynomial are now supported.

The program has other options, such as color distance, optimization initial value. You can view the comments of the program.

The program is different from the Imatest software in terms of linearization and optimization initialization. The results of the program are compared with the results of Imatest, and most of them are consistent, especially the calculation results of the ccm matrix. But some results are quite different.

You can test with the 'test.py' file.

