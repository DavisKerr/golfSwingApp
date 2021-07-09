import csv

class CSV_Creator:
    
    def __init__(self, points):
        self.points = points

    def generate_csv(self, destination):
        frame_numbers = [len(self.points[key]) for key in self.points.keys()]
        num_frames = min(frame_numbers)
        fieldnames = self.get_headings()
        rows = []
        for frame in range(0, num_frames):
            rows.append(self.get_row(frame))
        print(rows)
        with open(destination, mode="w", newline="") as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def get_headings(self):
        headings = []
        for key in self.points.keys():
            headings.append("x" + str(key))
            headings.append("y" + str(key))
        return headings

    def get_row(self, row_num):
        row = {}
        for key in self.points.keys():
            if self.points[key][row_num]:
                x_row_id = "x" + str(key)
                y_row_id = "y" + str(key)
                row[x_row_id] = self.points[key][row_num][0]
                row[y_row_id] = self.points[key][row_num][1]
        return row
