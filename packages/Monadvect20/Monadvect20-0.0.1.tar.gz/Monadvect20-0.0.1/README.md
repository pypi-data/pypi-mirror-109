Библиотека Monad предназначена для реализации основных монад в Python, а именно:

Монада Maybe, которая возврощает значение типа MaybeX, где X - тип значения (int,str,float), либо значение Nothing.
Обработка значений происходит с помощью >> (bind):

MaybeInt(5) >> function #возведение в квадрат
>>> 25 # тип значения - MaybeInt, при невозможности обработки значений --
>>> Nothing 

Монада Either при правильной обработки значений возвращает тип EitherX, при ошибке - Left

EitehInt(5) >> function
>>> 25 # тип EitherInt
>>> 5 # тип Left (при ошибке)

Монада Error возвращает тип ErrorX при отсутствии ошибки или (a, er), где a - значение, а er - тип ошибки (тип Failure)

ErrorInt(5) >> function
>>> 25 
>>> (5, TypeError) # тип Failure

Монада IO всегда возвращает значение тип str, либо ошибку типа IO_false

IO('5') >> fnStr # fnStr --> x + 'Test'
>>> '5Test'
>>> IO Monad Error: // тип ошибки // 

Монада List возваращет либо пустой MonadoList (при ошибке), либо с какими-либо значениями

MonadoList([1,2,3]) >> function
>>> [1,4,9]
>>> [] # при ошибке

Функция convectM преобразует обычное значение в нужную монаду

convectM(obj,pClass),где obj - значение, pClass - монадический класс
convectM(5,MaybeInt)
>>> 5 # тип - MaybeInt
