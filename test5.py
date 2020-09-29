# 物品类
class Dongxi:
    def __init__(self, name, weight, value):
        self.name = name
        self.weight = weight
        self.value = value
    def __str__(self):
        return self.name
# 背包类    
class Bag:
    def __init__(self, volume):
        self.volume  = volume

# Initial 函数用来，初始化参数
# 即根据几个name,weight,value的list来创建对应的对象，返回一个list 
# list里是对象们，也就是很多 Dongxi

def Initial(name,weight,value):
    list_of_thing = []
    for i in range(len(name)):
        list_of_thing.append(Dongxi(name[i],weight[i],value[i]))
    return list_of_thing

# 这个函数是为了计算一个list里的对象的总价值有多少而创建的
def value_sum(a_list):
    if type(a_list) != list:
        a_list = [a_list]
    return sum([x.value for x in a_list])

# 该begin函数是实施动态规划过程的函数
def begin(list1, bag1,None_type):
    # 类似地，我们创建的dataframe比包容量多1列
    # 比dongxi的个数多一行，这样方便动态规划的操作

    mat1 = pd.DataFrame(np.array([None_type]*(len(list1)+1)*(bag1.volume+1)).reshape(len(list1)+1, bag1.volume+1))
    # 为了方便起见，把dataframe里的所有都elements都变成list
    for i in range(mat1.shape[0]):
        mat1.loc[i,:] = mat1.loc[i,:].apply(lambda x:list(set([x])))

    for i in range(1, mat1.shape[0]):
        for j in range(1, mat1.shape[1]):
            if  j < list1[i-1].weight:
                # dataframe的赋值操作在这里要用copy()来执行，是dataframe自带的一种方法；
                # 否则新cell的改变也会反馈到原cell里
                mat1.loc[i, j] = mat1.loc[i-1, j].copy()
            else:
                if value_sum(mat1.loc[i-1,j]) >= value_sum(mat1.loc[i-1, j-list1[i-1].weight]) + list1[i-1].value:
                    mat1.loc[i,j] = mat1.loc[i-1,j].copy()
                else:
                    mat1.loc[i,j] = mat1.loc[i-1, j-list1[i-1].weight].copy()
                    mat1.loc[i,j].append(list1[i-1])
                    if None_type in mat1.loc[i,j] and len(mat1.loc[i,j]) > 1:
                        mat1.loc[i,j].remove(None_type)
    return mat1