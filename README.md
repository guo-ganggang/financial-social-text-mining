# financial-social-text-mining

金融讨论文本反应投资主体的心理活动与行为特征，而投资者的心理因素已经被证明是股票横截面收益的重要影响因素之一，对股价的生成机理与波动规则有重要影响。因此，通过金融文本语义挖掘，可以揭示投资者对上市公司战略的态度与反馈，以及对股票未来走势的预期。

文本提出的金融文本语义挖掘框架用来挖掘金融领域的一些知识与结论，所以在分析方法论上，借鉴经济学的比较方法和分析视角，分析的粒度定为宏观、中观与微观三类视角，对比的方法设定为横向和纵向两类方式。具
体来讲，就是应用挖掘技术时，要综合三个层次、两个类别来系统考虑，比如，从全部上市公司角度考虑宏观，从全行业角度考虑中观，从单个上市公司角度考虑微观；横向比较同类型企业，纵向比较同一企业不同发展阶段的情况。按照上述原则，共形成六个象限，依次挖掘六个象限共同支持同一结论，才能充分说明该结论或者知识模式的可靠性。每个象限挖掘的主体技术框架是可伸缩的，一般情况下，首先，通过LDA 主题模型挖掘文本主题，利用TFIDF算法计算出文本的关键词，用以对文本进行初步勘探；其次，采用Word2vec 模型根据初步勘探的讯息，进一步发掘深层的关系，如以相似度反应的词语之间的共现关系等；最后，根据具体的应用场景设定判别算法，最终形成较为确定的知识结论。

以往金融领域相关应用场景中的分析研究，由于受到技术的限制，一般只能采用计量经济学中的方法，且只能针对数值型数据做些统计与分析，本框架巧妙地整合文本挖掘领域多个先进的技术，创造性地设计了可以用来分析金融文本挖掘的一套系统性的框架，扩充了同类问题的研究手段。同时，又针对性地借鉴经济学问题的研究范式和视角，为模型的应用价值和可靠性提供了保证。由于这种跨学科的深度融合框架，目前没有完全同类功能的参照模型，因此，对比优势是不言而喻的。
