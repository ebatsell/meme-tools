"""This script takes in a `points.json` from the tSNE script and determines which images are within a certain threshold of each other."""
# Note: expects the main key to be "points" and contain the list of points

# future optimization: use Rtree to build a spatial index, which would be much better performance over this n^2 algo
# question: does tSNE create values relative to the corpus or would it have the same output streaming? test this
# we could support a very large Rtree index I think, with just storing points and ids (or even the full image paths) if so

import json
import math


def distance(p1, p2):
	return math.sqrt((p2["point"][1] - p1["point"][1])**2 + (p2["point"][0] - p1["point"][0])**2)


def cluster(points_file, threshold=0.008):
	points = json.loads(points_file.read())
	point_groups = []
	points_remaining = set(range(len(points)))

	def find_neighbors(current_point, points_remaining):
		candidate_group = {current_point}
		for point in points_remaining:
			if distance(points[current_point], points[point]) < threshold:
				candidate_group.add(point)

		point_groups.append(candidate_group)
		points_remaining -= candidate_group

	while points_remaining:
		current_point = points_remaining.pop()
		find_neighbors(current_point, points_remaining)

	groups = [
		[points[point_idx]["path"] for point_idx in point_group]
		for point_group in point_groups
	]
	return groups


if __name__ == "__main__":
	points_file_name = "output.json"
	points_file = open(points_file_name, "r+")
	groups = cluster(points_file)
	# print(json.dumps(groups, indent=2))
	# for group in groups[0:200]:
	# 	if len(group) > 1:
	# 		print(f"open {' '.join(group)};")

	sorted_groups = sorted(groups, key=len, reverse=True)
	for group in sorted_groups[0:15]:
		print(f"open {' '.join(group)};")

	breakpoint()
	# print(json.dumps(sorted_groups, indent=2))
