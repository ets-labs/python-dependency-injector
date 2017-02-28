var disqus_shortname;
var disqus_identifier;
(function() {{
    var disqus_thread = $("#disqus_thread");
    disqus_shortname = disqus_thread.data('disqus-shortname');
    disqus_identifier = disqus_thread.data('disqus-identifier');
    var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
    dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
}})();
