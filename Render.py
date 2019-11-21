from jinja2 import FileSystemLoader, Environment

# Render class
class Processing:
    # Initialze data structure
    def __init__(self):
        self.images_records = dict()
        
    # Add image dictionary    
    def setImageID(self, imageID):
        self.images_records.setdefault(imageID, dict())
    # Set image result to dictionary    
    def setImageResults(self, imageID, API, output, result):
        self.images_records[imageID][API] = [output, result]

    def HTMLGenerator(self, table):
        loader = FileSystemLoader('.')
        env = Environment(loader = loader)
        template = env.get_template("Template.html")
        self.writeHTML(template.render(image_records = self.images_records, image_results = table))
        
    def writeHTML(self, html):
        with open('Output.html', 'w') as file:
            file.write(html)
        
# Testing        
if __name__ == "__main__":
    render = Processing()
    render.setImageID('RCN3349')
    render.setImageResults('RCN3349', "Amazon", [1,2,3,4,5], "TN +1")
    render.setImageResults('RCN3349', "IBM", [5,4,3,2,1], "FN +1")
    render.setImageID('RCN4349')
    render.setImageResults('RCN4349', "Google", [1,2,3,4,5], "TP +1")
    render.setImageResults('RCN4349', "Clarifai", [5,4,3,2,1], "FP +1")
    print(render.images_records)