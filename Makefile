all:
	yst

publish: all
	python build_rss.py > site/blog.rss
	rsync -avz site/* chris@wolffia:/var/www/

clean:
	rm -rf site/
