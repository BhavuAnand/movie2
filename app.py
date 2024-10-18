from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,template_folder='templates')

# Simulated movie list
movies = [
    {'id': 1, 'name': 'Inception', 'price': 10},
    {'id': 2, 'name': 'The Dark Knight', 'price': 12},
    {'id': 3, 'name': 'Interstellar', 'price': 15}
]

# Simulated reviews (for movie reviews page)
reviews = {
    1: [  # Inception reviews
        {'source': 'IMDb', 'rating': 8.8, 'comment': 'Great plot!'},
        {'source': 'Rotten Tomatoes', 'rating': 86, 'comment': 'Brilliant visuals.'}
    ],
    2: [  # The Dark Knight reviews
        {'source': 'IMDb', 'rating': 9.0, 'comment': 'Best superhero movie.'},
        {'source': 'Rotten Tomatoes', 'rating': 94, 'comment': 'Gripping and thrilling.'}
    ],
    3: [  # Interstellar reviews
        {'source': 'IMDb', 'rating': 8.6, 'comment': 'Mind-bending sci-fi!'},
        {'source': 'Rotten Tomatoes', 'rating': 72, 'comment': 'Visually stunning, but confusing at times.'}
    ]
}

# Home page - List of movies
@app.route('/')
def home():
    return render_template('home.html', movies=movies)

# Movie reviews page - Aggregated reviews for a selected movie
@app.route('/movie/<int:movie_id>')
def movie_reviews(movie_id):
    movie = next(movie for movie in movies if movie['id'] == movie_id)
    movie_reviews = reviews.get(movie_id, [])
    return render_template('movie_reviews.html', movie=movie, reviews=movie_reviews)

# Booking tickets for a movie
@app.route('/movie/<int:movie_id>/book', methods=['GET', 'POST'])
def book_ticket(movie_id):
    movie = next(movie for movie in movies if movie['id'] == movie_id)

    if request.method == 'POST':
        # Get the number of tickets selected by the user
        num_tickets = int(request.form['num_tickets'])
        total_price = movie['price'] * num_tickets
        
        # Redirect to checkout with booking details
        return redirect(url_for('checkout', movie_id=movie_id, num_tickets=num_tickets, total_price=total_price))
    
    return render_template('book_ticket.html', movie=movie)

# Checkout page
@app.route('/checkout')
def checkout():
    movie_id = int(request.args.get('movie_id'))
    num_tickets = int(request.args.get('num_tickets'))
    total_price = float(request.args.get('total_price'))
    
    movie = next(movie for movie in movies if movie['id'] == movie_id)
    
    return render_template('checkout.html', movie=movie, num_tickets=num_tickets, total_price=total_price)

# Confirmation page after successful booking
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
