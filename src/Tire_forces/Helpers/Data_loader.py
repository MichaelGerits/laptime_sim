import pandas as pd
import numpy as np


class TireDataLoader:
    """
    A dynamic data loader for tire testing CSV datasets.
    
    Filters out invalid data and organizes sweeps by operational parameters
    (camber angle `gamma` and vertical load `Fz`). Enables extracting 1D 
    and 2D setting slices across arbitrary tire channels (e.g., Fy vs alpha, 
    Fx vs kappa, Mz vs alpha).
    """

    def __init__(self, file_path, x_col, y_col, gamma_col='gamma_deg', fz_col='Fz_N'):
        self.file_path = file_path
        self.x_col = x_col
        self.y_col = y_col
        self.gamma_col = gamma_col
        self.fz_col = fz_col

        # Load CSV, ignoring comment headers, and drop any rows with NaN entries
        df = pd.read_csv(file_path, comment='#').dropna(how='any')

        #checking if the collumn names actually exist
        required = [x_col, y_col, gamma_col, fz_col]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}. Available: {list(df.columns)}")

        #round vertical force into bins (e.g., 498.3 N -> 500 N)
        df['Fz_nominal'] = df[self.fz_col].round(-2)

        #sort ny the x_collumn
        df = df.sort_values(by=x_col)

        # Store cleaned DataFrame internally
        self.df = df.reset_index(drop=True)

    # =========================================================================
    # Inspection Properties & Methods
    # =========================================================================

    
        """Returns a sorted NumPy array of all available camber angles (gamma)."""
        self.gammas = np.sort(self.df[self.gamma_col].unique())
    
        """Returns a sorted NumPy array of all available nominal vertical loads (Fz)."""
        self.fzs = np.sort(self.df['Fz_nominal'].unique())

        self.collumns = list(self.df.columns)

    def show_summary(self):
        """Prints a human-readable summary of selectable parameters and dataset metrics."""
        print("=== Tire Dataset Selection Summary ===")
        print(f"Channels (columns) : {self.collumns}")
        print(f"Selectable Gammas  : {list(self.gammas)}")
        print(f"Selectable Fz [N]  : {list(self.fzs)}")

    # =========================================================================
    # Data Slice Extraction Methods
    # =========================================================================
    def data_get_gamma(self, gamma):
        
        if gamma not in self.gammas:
            raise ValueError(f"gamma {gamma} not in {self.gammas}")

        data = {}
        gamma_set = self.df[self.df[self.gamma_col] == gamma]

        for Fz in self.fzs:
            subset = gamma_set[gamma_set["Fz_nominal"] == Fz]
            data[Fz] = {
                self.x_col: np.array(subset[self.x_col].values),
                self.y_col: np.array(subset[self.y_col].values)
            }
        return data
    
    def data_get_fz(self, load_vert):

        if load_vert not in self.fzs:
            raise ValueError(f"gamma {load_vert} not in {self.fzs}")
        
        data = {}
        fz_set = self.df[self.df[self.fz_col] == load_vert]

        for gamma in self.gammas:
            subset = fz_set[fz_set[self.gamma_col] == gamma]
            data[gamma] = {
                self.x_col: np.array(subset[self.x_col].values),
                self.y_col: np.array(subset[self.y_col].values)
            }
        return data


