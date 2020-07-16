## Color Distance

The color distance quantifies the color difference of human perception.  

Generally, we use the CIE76, CIE94, or CIEDE2000 standard proposed by International Commission on illumination (CIE). They all need to convert the color space into the CIE lab space before calculating with the mathematical formulas [1]. There are some discontinuities in the formula of CIEDE2000, see [2] for details.

The program provides support for the CMC l:c (1984) distance. See formulas details in [1].

In addition, two simple distances are provided for reference. One is the RGB color space distance: 

$$
distance_{RGB}=\sqrt{(R_1-R_2)^2+(G_1-G_2)^2+(B_1-B_2)^2}
$$

and the linear RGB color space distance: 

$$
distance_{RGBL}=\sqrt{(R_{l1}-R_{l2})^2+(G_{l1}-G_{l2})^2+(B_{l1}-B_{l2})^2}
$$

The former is useful in machine vision, while the latter is simple and can be used as an initial value for other color difference fitting. 

## ColorChecker

The ColorChecker is used as the reference colors in color correction. All the colors of the color card have been calibrated in advance. The most popular standard ColorChecker is the Macbeth ColorChecker, which consists of 4 x 6 patches, as shown in Figure [3]. The patches in the last row is gray and can be used for grayscale linearization or white balance. 

The Macbeth ColorChecker CIE Lab values for 2 deg D50 illuminant have been calibrated by multiple people, and the results are different from each other[4–5]. The 2 deg D65 illuminant values can be obtained by measurement or chromatic adaptation. This program supports the Mecbeth ColorChecker, the 2 deg D50 values and D65 values come from [6]. Note that the chromatic adaptation result is different from the program values. 

In addition,  X-Rite also produces a variety of other ColorChecker[7]. 

The program supports the customization of the ColorChecker, and supports the input of gray positions. 

![File:Gretag-Macbeth ColorChecker.jpg](https://upload.wikimedia.org/wikipedia/commons/a/ad/Gretag-Macbeth_ColorChecker.jpg)

## Grayscale

Normally, grayscale is determined by the Y component of the CIE XYZ color space[8]. Therefore, the conversion from linear sRGB to linear grayscale is:
$$
G_{l}=0.2126R_l+0.7152G_l+0.0722B_l
$$
where subscript $l$  represents linear.

The color space of the detected data is not determined before color correction and cannot be converted into the XYZ space. Therefore, the sRGB formula is used to approximate[5]. 
$$
G=0.2126R+0.7152G+0.0722B
$$

## References

1. https://en.wikipedia.org/wiki/Color_difference
2. Sharma, Gaurav; Wu, Wencheng; Dalal, Edul N. (2005). ["The CIEDE2000 color-difference formula: Implementation notes, supplementary test data, and mathematical observations"](http://www.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf) (PDF). *Color Research & Applications*. [Wiley Interscience](https://en.wikipedia.org/wiki/Wiley_Interscience). **30** (1): 21–30. [doi](https://en.wikipedia.org/wiki/Doi_(identifier)):[10.1002/col.20070](https://doi.org/10.1002%2Fcol.20070)
3. https://en.wikipedia.org/wiki/ColorChecker
4. http://www.babelcolor.com/colorchecker.htm
5. https://xritephoto.com/ph_product_overview.aspx/?ID=938&Action=Support&SupportID=5884
6. https://www.imatest.com/wp-content/uploads/2011/11/Lab-data-Iluminate-D65-D50-spectro.xls
7. https://xritephoto.com/
8. https://en.wikipedia.org/wiki/Grayscale
