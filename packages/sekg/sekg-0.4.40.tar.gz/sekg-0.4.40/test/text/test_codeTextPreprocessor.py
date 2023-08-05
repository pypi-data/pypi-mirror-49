from unittest import TestCase

from sekg.text.util import CodeTextPreprocessor


class TestCodeTextPreprocessor(TestCase):
    def test_clean_html_text(self):
        html_text = """
<!doctype html>
<html>
  <head>
    <!-- MathJax -->
    <script type="text/javascript"
      src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
    <title>
      Caffe | Bias Layer
    </title>

    <link rel="icon" type="image/png" href="/images/caffeine-icon.png">

    <link rel="stylesheet" href="/stylesheets/reset.css">
    <link rel="stylesheet" href="/stylesheets/styles.css">
    <link rel="stylesheet" href="/stylesheets/pygment_trac.css">

    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
    <!--[if lt IE 9]>
    <script src="//html5shiv.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>
  <body>
  <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-46255508-1', 'daggerfs.com');
    ga('send', 'pageview');
  </script>
    <div class="wrapper">
      <header>
        <h1 class="header"><a href="/">Caffe</a></h1>
        <p class="header">
          Deep learning framework by <a class="header name" href="http://bair.berkeley.edu/">BAIR</a>
        </p>
        <p class="header">
          Created by
          <br>
          <a class="header name" href="http://daggerfs.com/">Yangqing Jia</a>
          <br>
          Lead Developer
          <br>
          <a class="header name" href="http://imaginarynumber.net/">Evan Shelhamer</a>
        <ul>
          <li>
            <a class="buttons github" href="https://github.com/BVLC/caffe">View On GitHub</a>
          </li>
        </ul>
      </header>
      <section>

      <h1 id="bias-layer">Bias Layer</h1>

<ul>
  <li>Layer type: <code class="highlighter-rouge">Bias</code></li>
  <li><a href="http://caffe.berkeleyvision.org/doxygen/classcaffe_1_1BiasLayer.html">Doxygen Documentation</a></li>
  <li>Header: <a href="https://github.com/BVLC/caffe/blob/master/include/caffe/layers/bias_layer.hpp"><code class="highlighter-rouge">./include/caffe/layers/bias_layer.hpp</code></a></li>
  <li>CPU implementation: <a href="https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bias_layer.cpp"><code class="highlighter-rouge">./src/caffe/layers/bias_layer.cpp</code></a></li>
  <li>CUDA GPU implementation: <a href="https://github.com/BVLC/caffe/blob/master/src/caffe/layers/bias_layer.cu"><code class="highlighter-rouge">./src/caffe/layers/bias_layer.cu</code></a></li>
</ul>

<h2 id="parameters">Parameters</h2>
<ul>
  <li>Parameters (<code class="highlighter-rouge">BiasParameter bias_param</code>)</li>
  <li>From <a href="https://github.com/BVLC/caffe/blob/master/src/caffe/proto/caffe.proto"><code class="highlighter-rouge">./src/caffe/proto/caffe.proto</code></a>):</li>
</ul>

<figure class="highlight"><pre><code class="language-protobuf" data-lang="protobuf"><span class="kd">message</span> <span class="nc">BiasParameter</span> <span class="p">{</span>
  <span class="c1">// The first axis of bottom[0] (the first input Blob) along which to apply
</span>  <span class="c1">// bottom[1] (the second input Blob).  May be negative to index from the end
</span>  <span class="c1">// (e.g., -1 for the last axis).
</span>  <span class="c1">//
</span>  <span class="c1">// For example, if bottom[0] is 4D with shape 100x3x40x60, the output
</span>  <span class="c1">// top[0] will have the same shape, and bottom[1] may have any of the
</span>  <span class="c1">// following shapes (for the given value of axis):
</span>  <span class="c1">//    (axis == 0 == -4) 100; 100x3; 100x3x40; 100x3x40x60
</span>  <span class="c1">//    (axis == 1 == -3)          3;     3x40;     3x40x60
</span>  <span class="c1">//    (axis == 2 == -2)                   40;       40x60
</span>  <span class="c1">//    (axis == 3 == -1)                                60
</span>  <span class="c1">// Furthermore, bottom[1] may have the empty shape (regardless of the value of
</span>  <span class="c1">// "axis") -- a scalar bias.
</span>  <span class="k">optional</span> <span class="kt">int32</span> <span class="na">axis</span> <span class="o">=</span> <span class="mi">1</span> <span class="p">[</span><span class="k">default</span> <span class="o">=</span> <span class="mi">1</span><span class="p">];</span>

  <span class="c1">// (num_axes is ignored unless just one bottom is given and the bias is
</span>  <span class="c1">// a learned parameter of the layer.  Otherwise, num_axes is determined by the
</span>  <span class="c1">// number of axes by the second bottom.)
</span>  <span class="c1">// The number of axes of the input (bottom[0]) covered by the bias
</span>  <span class="c1">// parameter, or -1 to cover all axes of bottom[0] starting from `axis`.
</span>  <span class="c1">// Set num_axes := 0, to add a zero-axis Blob: a scalar.
</span>  <span class="k">optional</span> <span class="kt">int32</span> <span class="na">num_axes</span> <span class="o">=</span> <span class="mi">2</span> <span class="p">[</span><span class="k">default</span> <span class="o">=</span> <span class="mi">1</span><span class="p">];</span>

  <span class="c1">// (filler is ignored unless just one bottom is given and the bias is
</span>  <span class="c1">// a learned parameter of the layer.)
</span>  <span class="c1">// The initialization for the learned bias parameter.
</span>  <span class="c1">// Default is the zero (0) initialization, resulting in the BiasLayer
</span>  <span class="c1">// initially performing the identity operation.
</span>  <span class="k">optional</span> <span class="n">FillerParameter</span> <span class="na">filler</span> <span class="o">=</span> <span class="mi">3</span><span class="p">;</span>
<span class="p">}</span></code></pre></figure>



      </section>
  </div>
  </body>
</html>
"""
        preprocessor = CodeTextPreprocessor()
        clean = preprocessor.clean_html_text(html_text=html_text)
        print(clean)
