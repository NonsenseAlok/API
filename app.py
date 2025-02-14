from flask import Flask, request, jsonify

app = Flask(__name__)

cost_matrix = {
    "C1_L1": 20, "C2_L1": 30, "C3_L1": 40,
    "C1_C2": 10, "C2_C3": 15, "C1_C3": 25
}
warehouse_stock = {
    "C1": ["A", "B", "C"],
    "C2": ["D", "E", "F"],
    "C3": ["G", "H", "I"]
}


def calculate_minimum_cost(order):
    centers_required = set()
    for item in order.keys():
        for center, products in warehouse_stock.items():
            if item in products:
                centers_required.add(center)
                break

    if len(centers_required) == 1:
        center = list(centers_required)[0]
        return cost_matrix[f"{center}_L1"]

    min_cost = float('inf')
    for start_center in centers_required:
        cost = cost_matrix[f"{start_center}_L1"]
        remaining_centers = centers_required - {start_center}
        for other_center in remaining_centers:
            cost += cost_matrix[f"{start_center}_{other_center}"]
            cost += cost_matrix[f"{other_center}_L1"]
        min_cost = min(min_cost, cost)

    return min_cost


@app.route('/calculate_cost', methods=['POST'])
def calculate_cost():
    try:
        order = request.json
        min_cost = calculate_minimum_cost(order)
        return jsonify({"minimum_cost": min_cost})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
