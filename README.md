This repo is to implement color adjustment algorithm based on colorchecker.

The main idea of the algorithm is as follows: input a picture with a colorchecker, linearize the input colorchecker colors, and then use the color correction matrix(CCM) to linearly transform the former result to minimize the distance from the standard colorchecker colors. The goal of optimization is the ccm matrix.

After the ccm matrix is calculated, you can enter the picture for correction. The input picture is linearized, then multiplied by the ccm matrix, and then inversely linearized. Note that the rules for linearization and delinearization may be different.

Several linearization mechanisms such as gamma, sgrb, and polynomial are now supported.

The program has other options, such as color distance, optimization initial value. You can view the comments of the program.

The program is different from the Imatest software in terms of linearization and optimization initialization. The results of the program are compared with the results of Imatest, and most of them are consistent, especially the calculation results of the ccm matrix. But some results are quite different.

You can test with the 'test.py' file. The input colorchecker colors is got from Imatest software. The 'input1.png' test file is from http://cvil.eecs.yorku.ca/projects/public_html/sRGB_WB_correction/dataset.html, and 'input2.png' test file is from https://www2.cs.sfu.ca/~colour/data/shi_gehler/. 

There will be more functions in branch v2.

- [x] weights
- [x] color space
- [x] new linearize class
- [x] accept customerized colorchecker
- [x] new ccm matrix
- [x] new distance function
- [x] rgb or bgr (determined: only rgb)

Future functions:

- [ ] value linearization functions (discard)
- [x] value optimization
- [ ] auto gamma (discard)
- [ ] auto optimization (discard)
- [ ] average RGB CS density, including relative detection