import Paper from "@mui/material/Paper";
import { ExpandLess, ExpandMore } from "@mui/icons-material";
import Collapse from "@mui/material/Collapse";
import SearchBar from "booksearch/SearchBar/SearchBar";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import { useState } from "react";
import TextField from "@mui/material/TextField";
import { Autocomplete } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";
import Button from "@mui/material/Button";
import api from "api";
import PropTypes from "prop-types";

function AdvancedSearch(props) {
    const [open, setOpen] = useState(false);

    const handleAdvancedClick = () => {
        setOpen(!open);
    };

    const categories = ["Home Economics", "Fiction", "Science"]; // TODO fetch this from the backend

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

    const onSearch = async (value) => {
        props.onStartSearch();
        api.get("search", {
            text: value,
        })
            .then((response) => {
                props.onSearch(response.data);
            })
            .catch(() => {
                props.onError();
            });
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
                                    label="Released after"
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
                                    label="Released before"
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
                                {/* TODO size is wrong */}
                                <Autocomplete
                                    disablePortal
                                    id="category"
                                    options={categories}
                                    renderInput={(params) => (
                                        <TextField
                                            {...params}
                                            label="Category"
                                            sx={{
                                                input: { color: "#FFFFFF" },
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
                                        input: { color: "#FFFFFF" },
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
                                    label="Alive after"
                                    inputFormat="DD/MM/YYYY"
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
                                    label="Alive before"
                                    inputFormat="DD/MM/YYYY"
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
                        <Button variant="contained" sx={{ color: "#FFFFFF", marginTop: "1.5em" }}>
                            Search
                        </Button>
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
