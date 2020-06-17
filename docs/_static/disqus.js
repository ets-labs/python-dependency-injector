$(function() {
    var disqus_thread = $("#disqus_thread");
    var disqus_shortname = disqus_thread.data('disqus-shortname');
    var disqus_identifier = disqus_thread.data('disqus-identifier');
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
});
