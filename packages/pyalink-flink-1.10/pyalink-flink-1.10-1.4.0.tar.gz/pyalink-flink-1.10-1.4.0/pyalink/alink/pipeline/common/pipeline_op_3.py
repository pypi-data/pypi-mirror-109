#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..base import Estimator, Transformer, Model, TuningEvaluator
from ..tuning.base import BaseGridSearch, BaseRandomSearch
from ..lazy.has_lazy_print_model_info import HasLazyPrintModelInfo
from ..lazy.has_lazy_print_train_info import HasLazyPrintTrainInfo
from ..local_predictor import LocalPredictable


class LdaModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.clustering.LdaModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LdaModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class LinearRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LinearRegressionModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.LinearRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class LinearSvm(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvm'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvm, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LinearSvmModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LinearSvmModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LinearSvmModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class LogisticRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LogisticRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class LogisticRegressionModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.LogisticRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(LogisticRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class Lookup(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.Lookup'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Lookup, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMapKeyCols(self, val):
        return self._add_param('mapKeyCols', val)

    def setMapValueCols(self, val):
        return self._add_param('mapValueCols', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setModelStreamUpdateMethod(self, val):
        return self._add_param('modelStreamUpdateMethod', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class MaxAbsScaler(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MaxAbsScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MaxAbsScalerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MaxAbsScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MaxAbsScalerModel, self).__init__(*args, **kwargs)
        pass

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MinMaxScaler(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MinMaxScaler'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScaler, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setMax(self, val):
        return self._add_param('max', val)

    def setMin(self, val):
        return self._add_param('min', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MinMaxScalerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MinMaxScalerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MinMaxScalerModel, self).__init__(*args, **kwargs)
        pass

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)


class MultiClassClassificationTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.MultiClassClassificationTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiClassClassificationTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setTuningMultiClassMetric(self, val):
        return self._add_param('tuningMultiClassMetric', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)


class MultiHotEncoder(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.MultiHotEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiHotEncoder, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDelimiter(self, val):
        return self._add_param('delimiter', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class MultiHotEncoderModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.MultiHotEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiHotEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class MultiStringIndexer(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MultiStringIndexer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStringOrderType(self, val):
        return self._add_param('stringOrderType', val)


class MultiStringIndexerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.dataproc.MultiStringIndexerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultiStringIndexerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class MultilayerPerceptronClassificationModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.MultilayerPerceptronClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class MultilayerPerceptronClassifier(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.MultilayerPerceptronClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(MultilayerPerceptronClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLayers(self, val):
        return self._add_param('layers', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setBlockSize(self, val):
        return self._add_param('blockSize', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setInitialWeights(self, val):
        return self._add_param('initialWeights', val)

    def setL1(self, val):
        return self._add_param('l1', val)

    def setL2(self, val):
        return self._add_param('l2', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class NGram(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.NGram'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NGram, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setN(self, val):
        return self._add_param('n', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class NaiveBayes(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayes'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayes, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSmoothing(self, val):
        return self._add_param('smoothing', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class NaiveBayesModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayesModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class NaiveBayesTextClassifier(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayesTextClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextClassifier, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setModelType(self, val):
        return self._add_param('modelType', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSmoothing(self, val):
        return self._add_param('smoothing', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class NaiveBayesTextModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.NaiveBayesTextModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(NaiveBayesTextModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneHotEncoder(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.OneHotEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotEncoder, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDiscreteThresholds(self, val):
        return self._add_param('discreteThresholds', val)

    def setDiscreteThresholdsArray(self, val):
        return self._add_param('discreteThresholdsArray', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneHotEncoderModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.OneHotEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneHotEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneVsRest(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRest'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneVsRest, self).__init__(*args, **kwargs)
        pass

    def setNumClass(self, val):
        return self._add_param('numClass', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class OneVsRestModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.OneVsRestModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(OneVsRestModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class PCA(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCA'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCA, self).__init__(*args, **kwargs)
        pass

    def setK(self, val):
        return self._add_param('k', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCalculationType(self, val):
        return self._add_param('calculationType', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class PCAModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.PCAModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(PCAModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class QuantileDiscretizer(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setLeftOpen(self, val):
        return self._add_param('leftOpen', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumBuckets(self, val):
        return self._add_param('numBuckets', val)

    def setNumBucketsArray(self, val):
        return self._add_param('numBucketsArray', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class QuantileDiscretizerModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.QuantileDiscretizerModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(QuantileDiscretizerModel, self).__init__(*args, **kwargs)
        pass

    def setSelectedCols(self, val):
        return self._add_param('selectedCols', val)

    def setDropLast(self, val):
        return self._add_param('dropLast', val)

    def setEncode(self, val):
        return self._add_param('encode', val)

    def setHandleInvalid(self, val):
        return self._add_param('handleInvalid', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCols(self, val):
        return self._add_param('outputCols', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class RandomForestClassificationModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassificationModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassificationModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class RandomForestClassifier(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.classification.RandomForestClassifier'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestClassifier, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setPredictionDetailCol(self, val):
        return self._add_param('predictionDetailCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class RandomForestEncoder(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestEncoder, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setFeatureSubsamplingRatio(self, val):
        return self._add_param('featureSubsamplingRatio', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setNumTreesOfGini(self, val):
        return self._add_param('numTreesOfGini', val)

    def setNumTreesOfInfoGain(self, val):
        return self._add_param('numTreesOfInfoGain', val)

    def setNumTreesOfInfoGainRatio(self, val):
        return self._add_param('numTreesOfInfoGainRatio', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class RandomForestEncoderModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class RandomForestRegEncoder(Estimator):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestRegEncoder'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegEncoder, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class RandomForestRegEncoderModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.feature.RandomForestRegEncoderModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegEncoderModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class RandomForestRegressionModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)


class RandomForestRegressor(Estimator, HasLazyPrintModelInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RandomForestRegressor'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomForestRegressor, self).__init__(*args, **kwargs)
        pass

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setCategoricalCols(self, val):
        return self._add_param('categoricalCols', val)

    def setCreateTreeMode(self, val):
        return self._add_param('createTreeMode', val)

    def setMaxBins(self, val):
        return self._add_param('maxBins', val)

    def setMaxDepth(self, val):
        return self._add_param('maxDepth', val)

    def setMaxLeaves(self, val):
        return self._add_param('maxLeaves', val)

    def setMaxMemoryInMB(self, val):
        return self._add_param('maxMemoryInMB', val)

    def setMinInfoGain(self, val):
        return self._add_param('minInfoGain', val)

    def setMinSampleRatioPerChild(self, val):
        return self._add_param('minSampleRatioPerChild', val)

    def setMinSamplesPerLeaf(self, val):
        return self._add_param('minSamplesPerLeaf', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumSubsetFeatures(self, val):
        return self._add_param('numSubsetFeatures', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setNumTrees(self, val):
        return self._add_param('numTrees', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setSeed(self, val):
        return self._add_param('seed', val)

    def setSubsamplingRatio(self, val):
        return self._add_param('subsamplingRatio', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)


class RandomSearchCV(BaseRandomSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchCV'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchCV, self).__init__(*args, **kwargs)
        pass

    def setNumFolds(self, val):
        return self._add_param('NumFolds', val)

    def setNumIter(self, val):
        return self._add_param('numIter', val)


class RandomSearchCVModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchCVModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchCVModel, self).__init__(*args, **kwargs)
        pass


class RandomSearchTVSplit(BaseRandomSearch, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchTVSplit'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchTVSplit, self).__init__(*args, **kwargs)
        pass

    def setNumIter(self, val):
        return self._add_param('numIter', val)

    def setTrainRatio(self, val):
        return self._add_param('trainRatio', val)


class RandomSearchTVSplitModel(Model):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RandomSearchTVSplitModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RandomSearchTVSplitModel, self).__init__(*args, **kwargs)
        pass


class RegexTokenizer(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.RegexTokenizer'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegexTokenizer, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setGaps(self, val):
        return self._add_param('gaps', val)

    def setMinTokenLength(self, val):
        return self._add_param('minTokenLength', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setPattern(self, val):
        return self._add_param('pattern', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setToLowerCase(self, val):
        return self._add_param('toLowerCase', val)


class RegressionTuningEvaluator(TuningEvaluator):
    CLS_NAME = 'com.alibaba.alink.pipeline.tuning.RegressionTuningEvaluator'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RegressionTuningEvaluator, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setTuningRegressionMetric(self, val):
        return self._add_param('tuningRegressionMetric', val)


class RidgeRegression(Estimator, HasLazyPrintModelInfo, HasLazyPrintTrainInfo):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegression'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegression, self).__init__(*args, **kwargs)
        pass

    def setLabelCol(self, val):
        return self._add_param('labelCol', val)

    def setLambda(self, val):
        return self._add_param('lambda', val)

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setEpsilon(self, val):
        return self._add_param('epsilon', val)

    def setFeatureCols(self, val):
        return self._add_param('featureCols', val)

    def setMaxIter(self, val):
        return self._add_param('maxIter', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOptimMethod(self, val):
        return self._add_param('optimMethod', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setStandardization(self, val):
        return self._add_param('standardization', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)

    def setWeightCol(self, val):
        return self._add_param('weightCol', val)

    def setWithIntercept(self, val):
        return self._add_param('withIntercept', val)


class RidgeRegressionModel(Model, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.regression.RidgeRegressionModel'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(RidgeRegressionModel, self).__init__(*args, **kwargs)
        pass

    def setPredictionCol(self, val):
        return self._add_param('predictionCol', val)

    def setModelStreamFilePath(self, val):
        return self._add_param('modelStreamFilePath', val)

    def setModelStreamScanInterval(self, val):
        return self._add_param('modelStreamScanInterval', val)

    def setModelStreamStartTime(self, val):
        return self._add_param('modelStreamStartTime', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setVectorCol(self, val):
        return self._add_param('vectorCol', val)


class Segment(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.nlp.Segment'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Segment, self).__init__(*args, **kwargs)
        pass

    def setSelectedCol(self, val):
        return self._add_param('selectedCol', val)

    def setNumThreads(self, val):
        return self._add_param('numThreads', val)

    def setOutputCol(self, val):
        return self._add_param('outputCol', val)

    def setReservedCols(self, val):
        return self._add_param('reservedCols', val)

    def setUserDefinedDict(self, val):
        return self._add_param('userDefinedDict', val)


class Select(Transformer, LocalPredictable):
    CLS_NAME = 'com.alibaba.alink.pipeline.sql.Select'
    OP_TYPE = 'FUNCTION'

    def __init__(self, *args, **kwargs):
        kwargs['CLS_NAME'] = self.CLS_NAME
        kwargs['OP_TYPE'] = self.OP_TYPE
        super(Select, self).__init__(*args, **kwargs)
        pass

    def setClause(self, val):
        return self._add_param('clause', val)

