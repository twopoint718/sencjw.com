all:
	yst

github: all site/blog.rss
	cd site
	git commit -am "publish"
	git push
	cd ..

publish: all site/blog.rss
	rsync -avz site/* chris@wolffia:/var/www/

site/blog.rss: posts.yaml
	python build_rss.py > site/blog.rss
