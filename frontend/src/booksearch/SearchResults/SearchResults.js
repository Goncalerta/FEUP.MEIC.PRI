import PropTypes from "prop-types";

function SearchResults(props) {
    const { loading, error, data } = props;

    return (
        <div>
            RESULTS <br />
            {loading && <p>Loading...</p>}
            {error && <p>Error</p>}
            {!loading && !error && data.length === 0 && <p>No results</p>}
            {!loading && !error && data.map((book) => <div key={book.id}>{book.title}</div>)}
        </div>
    );
}

SearchResults.propTypes = {
    loading: PropTypes.bool.isRequired,
    error: PropTypes.bool.isRequired,
    data: PropTypes.array.isRequired /* eslint-disable-line react/forbid-prop-types */,
};

export default SearchResults;
