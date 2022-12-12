import Paper from "@mui/material/Paper";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import Collapse from "@mui/material/Collapse";
import SearchBar from "booksearch/SearchBar/SearchBar";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import { useEffect, useState } from "react";
import TextField from "@mui/material/TextField";
import { Autocomplete } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";
import api from "api";
import PropTypes from "prop-types";
import MKButton from "components/MKButton";

function AdvancedSearch(props) {
    const [open, setOpen] = useState(false);

    const [categories, setCategories] = useState([
        "Pastoral poetry",
        "English poetry -- 18th century",
        "Humorous stories",
        "England -- Fiction",
        "Short stories, English -- Periodicals",
        "English literature -- Periodicals",
    ]);

    const handleAdvancedClick = () => {
        setOpen(!open);
    };

    const fetchCategories = async () => {
        try {
            const response = await api.get("categories", {});
            if (response.status === 200) {
                setCategories(response.data);
            } else {
                console.log("Failed to fetch categories");
            }
        } catch (e) {
            console.log(e);
        }
    };

    useEffect(() => fetchCategories(), []);

    const [fromReleaseDate, setFromReleaseDate] = useState(null);

    const handleFromReleaseDate = (newValue) => {
        setFromReleaseDate(newValue);
    };

    const [toReleaseDate, setToReleaseDate] = useState(null);

    const handleToReleaseDate = (newValue) => {
        setToReleaseDate(newValue);
    };

    const [authorAliveBeginDate, setAuthorAliveBeginDate] = useState(null);

    const handleAuthorAliveBeginDate = (newValue) => {
        setAuthorAliveBeginDate(newValue);
    };

    const [authorAliveEndDate, setAuthorAliveEndDate] = useState(null);

    const handleAuthorAliveEndDate = (newValue) => {
        setAuthorAliveEndDate(newValue);
    };

    const onAdvancedSearch = () => {
        props.onStartSearch();
        api.get("advancedSearch", {
            params: {
                value:
                    document.getElementById("searchBar").value !== ""
                        ? document.getElementById("searchBar").value
                        : null,
                title:
                    document.getElementById("title").value !== ""
                        ? document.getElementById("title").value
                        : null,
                releasedAfter: fromReleaseDate ? fromReleaseDate.format() : null,
                releasedBefore: toReleaseDate ? toReleaseDate.format() : null,
                category:
                    document.getElementById("category").value !== ""
                        ? document.getElementById("category").value
                        : null,
                ratingMin:
                    document.getElementById("rating-min").value !== ""
                        ? document.getElementById("rating-min").value
                        : null,
                ratingMax:
                    document.getElementById("rating-max").value !== ""
                        ? document.getElementById("rating-max").value
                        : null,
                minNumRating:
                    document.getElementById("min-num-rating").value !== ""
                        ? document.getElementById("min-num-rating").value
                        : null,
                maxNumRating:
                    document.getElementById("max-num-rating").value !== ""
                        ? document.getElementById("max-num-rating").value
                        : null,
                authorFirstName:
                    document.getElementById("author-first-name").value !== ""
                        ? document.getElementById("author-first-name").value
                        : null,
                authorLastName:
                    document.getElementById("author-last-name").value !== ""
                        ? document.getElementById("author-last-name").value
                        : null,
                aliveAfter: authorAliveBeginDate ? authorAliveBeginDate.format() : null,
                aliveBefore: authorAliveEndDate ? authorAliveEndDate.format() : null,
            },
        })
            .then((response) => {
                props.onSearch(response.data);
            })
            .catch((e) => {
                console.log("Error", e);
                props.onError();
            });
    };

    const onSearch = (text) => {
        if (open) {
            return onAdvancedSearch();
        }
        if (text === "") {
            return null;
        }
        props.onStartSearch();
        api.get("search", {
            params: {
                value: text,
            },
        })
            .then((response) => {
                props.onSearch(response.data);
            })
            .catch((e) => {
                console.log("Error", e);
                props.onError();
            });
        return null;
    };

    return (
        <Paper
            component="form"
            sx={{
                p: "2px 4px",
                display: "flex",
                marginLeft: "auto",
                marginRight: "auto",
                alignItems: "center",
                width: "80%",
                flexDirection: "column",
                background: "transparent",
                boxShadow: "none",
            }}
        >
            <SearchBar onSearch={onSearch} />
            <Box
                onClick={handleAdvancedClick}
                style={{
                    marginLeft: "auto",
                    marginRight: "0.75em",
                    marginTop: "0.5em",
                    display: "flex",
                    alignItems: "center",
                    userSelect: "none",
                    color: "white",
                    cursor: "pointer",
                }}
            >
                Advanced {open ? <ExpandLess /> : <ExpandMore />}
            </Box>

            <Collapse in={open} timeout="auto" unmountOnExit>
                <LocalizationProvider dateAdapter={AdapterDayjs}>
                    <Box
                        style={{
                            flexGrow: 1,
                            background: "#00000090",
                            borderRadius: "1em",
                            padding: "1em 0.75em",
                            input: { color: "red" },
                        }}
                    >
                        <Grid container spacing={2}>
                            <Grid item xs={6}>
                                <TextField
                                    id="title"
                                    label="Title"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <DesktopDatePicker
                                    id="releasedAfter"
                                    label="Released after"
                                    minDate={new Date("01/01/1000")}
                                    maxDate={new Date("01/01/2100")}
                                    inputFormat="DD/MM/YYYY"
                                    value={fromReleaseDate}
                                    onChange={handleFromReleaseDate}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            sx={{
                                                input: { color: "#FFFFFF" },
                                                label: { color: "#FFFFFF" },
                                                svg: { color: "#FFFFFF" },
                                            }}
                                        />
                                    )}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <DesktopDatePicker
                                    id="releasedBefore"
                                    label="Released before"
                                    minDate={new Date("01/01/1000")}
                                    maxDate={new Date("01/01/2100")}
                                    inputFormat="DD/MM/YYYY"
                                    value={toReleaseDate}
                                    onChange={handleToReleaseDate}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            sx={{
                                                input: { color: "#FFFFFF" },
                                                label: { color: "#FFFFFF" },
                                                svg: { color: "#FFFFFF" },
                                            }}
                                        />
                                    )}
                                />
                            </Grid>
                            <Grid item xs={4}>
                                <Autocomplete
                                    freeSolo
                                    disablePortal
                                    id="category"
                                    options={categories}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            label="Category"
                                            sx={{
                                                input: {
                                                    height: "0.8em",
                                                    color: "#FFFFFF",
                                                },
                                                label: { color: "#FFFFFF" },
                                                svg: { color: "#FFFFFF" },
                                            }}
                                        />
                                    )}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <TextField
                                    id="rating-min"
                                    label="Min rating"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { height: "1.5em", color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                    inputProps={{ inputMode: "numeric", pattern: "[0-9]*" }}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <TextField
                                    id="rating-max"
                                    label="Max rating"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                    inputProps={{ inputMode: "numeric", pattern: "[0-9]*" }}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <TextField
                                    id="min-num-rating"
                                    label="Min # ratings"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                />
                            </Grid>
                            <Grid item xs={2}>
                                <TextField
                                    id="max-num-rating"
                                    label="Max # ratings"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <TextField
                                    id="author-first-name"
                                    label="Author first name"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <TextField
                                    id="author-last-name"
                                    label="Author last name"
                                    variant="outlined"
                                    sx={{
                                        width: "100%",
                                        input: { color: "#FFFFFF" },
                                        label: { color: "#FFFFFF" },
                                    }}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <DesktopDatePicker
                                    id="aliveAfter"
                                    label="Alive after"
                                    inputFormat="DD/MM/YYYY"
                                    minDate={new Date("01/01/1000")}
                                    maxDate={new Date("01/01/2100")}
                                    value={authorAliveBeginDate}
                                    onChange={handleAuthorAliveBeginDate}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            sx={{
                                                input: { color: "#FFFFFF" },
                                                label: { color: "#FFFFFF" },
                                                svg: { color: "#FFFFFF" },
                                            }}
                                        />
                                    )}
                                />
                            </Grid>
                            <Grid item xs={3}>
                                <DesktopDatePicker
                                    id="aliveBefore"
                                    label="Alive before"
                                    inputFormat="DD/MM/YYYY"
                                    minDate={new Date("01/01/1000")}
                                    maxDate={new Date("01/01/2100")}
                                    value={authorAliveEndDate}
                                    onChange={handleAuthorAliveEndDate}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            sx={{
                                                input: { color: "#FFFFFF" },
                                                label: { color: "#FFFFFF" },
                                                svg: { color: "#FFFFFF" },
                                            }}
                                        />
                                    )}
                                />
                            </Grid>
                        </Grid>
                        <MKButton
                            variant="contained"
                            sx={{ marginTop: "1.5em" }}
                            onClick={onAdvancedSearch}
                        >
                            Search
                        </MKButton>
                    </Box>
                </LocalizationProvider>
            </Collapse>
        </Paper>
    );
}

AdvancedSearch.propTypes = {
    onSearch: PropTypes.func.isRequired,
    onError: PropTypes.func.isRequired,
    onStartSearch: PropTypes.func.isRequired,
};

export default AdvancedSearch;
