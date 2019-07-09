import requests
import os
import json
import click 

class CLI(object):

    def __init__(self):
        pass

    def show_repositories(self,repo):
        """
        Docs:
        List all images from repo
        - Arguments: repo (repo name)
        """
        try:
            url = "https://" +  repo + "/v2/" + "_catalog?n=5000"
            r = requests.get(url)
            repos = r.json()
            return repos
        except requests.HTTPError as error:
            print(error)
    
    def show_tags(self,repo,image):
        """
        Docs:
        List all image tags
        - Arguments: repo, image
        """
        try:
            url = "https://" +  repo + "/v2/" + image + "/tags/list"
            r = requests.get(url)
            tags = r.json()
            return tags
        except requests.HTTPError as error:
            print(error)

    def pull(self,image):
        try:
            cmd = 'docker pull ' + image
            os.system(cmd)
        except AssertionError as error:
            print(error)

    def tag(self, *args):
        src_tag = args[0]
        dst_tag = args[1]
        try:
            cmd = 'docker tag ' + src_tag + " " + dst_tag
            os.system(cmd)
        except AssertionError as error:
            print(error)

    def push(self,image):
        try:
            cmd = 'docker push ' + image
            os.system(cmd)

        except AssertionError as error:
            print(error)

    def remove (self,image):
        try:
            cmd = 'docker rmi ' + image
            os.system(cmd)

        except AssertionError as error:
            print(error)
    def migration(self,*args):
        """
        Docs:
            migration image from old docker registry to the new one
            - Arguments: img,tag,src,dst
                img => image you wish to migration
                tag => image tag
                src => source repo
                dst =>  destination repo
        """
        img = args[0]
        tag = args[1]
        src = args[2]
        dst = args[3]
        old = src + "/" + img + ":" + tag
        new = dst + "/" + img + ":" + tag
        print("==============Image mirationing============== \nIMAGE: {} \nFORM : {} \nTO:  {}".format(img + ":" + tag,old,new))
        try:
            #Pull docker image
            self.pull(old)
            #Re-tags docker image
            self.tag(old, new)
            #Push docker image
            self.push(new)
            self.remove(old)
            self.remove(new)
        except AssertionError as error:
            print(error)
    
    def migration_repo(self, *args):
        src_repo = args[0]
        dst_repo = args[1]
        image    = args[2]
        try:
            tags = self.show_tags(src_repo,image)
            for tag in tags['tags']:
                #migration images
                self.migration(image,tag,src_repo,dst_repo)
        except AssertionError as error:
            print(error)

    def migration_all(self, *args):
        """
        Docs:
            migration all images from old docker registry to the new docker registry
            - Arguments: src_repo,dst_repo
                src_repo => the old docker registry (old-master-dr.lzd.co)
                dst_repo => the new docker registry (new-master-dr.lzd.co)
        """
        src_repo = args[0]
        dst_repo = args[1]
        try:
            images = self.show_repositories(src_repo)
            for image in images['repositories']:
                tags = self.show_tags(src_repo,image)
                for tag in tags['tags']:
                    #migration images
                    self.migration(image,tag,src_repo,dst_repo)
        except AssertionError as error:
            print(error)

    def help(self):
        print(
            "Usage: registry-cli.py [OPTIONS] [OPTIONS]... \n\n" +

            "Options:\n" + 
            "   show\n"
            "     show repo <repo name> \n"    
            "       Example: \n"
            "         python registry-cli.py show repo ro-master-dr.lzd.co \n" 
            "     show tag <repo> <image> \n"
            "       Example: \n"
            "         python registry-cli.py show tag ro-master-dr.lzd.co google_containers/pause\n"
            "   migration\n"
            "     migration <src repo> <dst repo>\n"
            "       Example: \n"
            "         python registry-cli.py migration <src repo> <dst repo>\n"
            "   help  Show this message and exit."
        )

    @click.command()
    @click.argument('options', nargs=-1)
    def run(options):
        cli  = CLI()
        try:
            if options[0] == 'show':
                if options[1] == 'tag':
                    tags = cli.show_tags(options[2],options[3])
                    print (json.dumps(tags,indent=4,sort_keys=True))

                elif options[1] == 'repo':
                    repos = cli.show_repositories(options[2])
                    print (json.dumps(repos,indent=4,sort_keys=True))
                else:
                    cli.help()

            elif options[0] == 'migration':
                if options[1] == 'all':
                    cli.migration_all(options[2],options[3])
                elif options[1] == 'repo':
                    cli.migration_repo(options[2],options[3],options[4])
                else:
                    cli.help()
            else:
                cli.help()
        except AssertionError as error:
            print(error)

if __name__ == '__main__':
    try:
        cli = CLI()
        cli.run()
        # cli.migration_repo('ro-master-dr.lzd.co','docker-registry.lel.asia','addresses/application')
    except KeyboardInterrupt:
        pass