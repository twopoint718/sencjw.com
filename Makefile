all:
	yst

publish: all
	rsync -avz site/* chris@wolffia:/var/www/

clean:
	rm -rf site/
