"""
Compliance service for calculating document status.
Handles RED/GREEN status calculation based on expiry dates.
"""
from datetime import datetime, timedelta


class ComplianceService:
    """
    Service for calculating compliance status of documents.
    
    Requirements: 5.3, 5.4
    """
    
    @staticmethod
    def calculate_status(expiry_date):
        """
        Calculate compliance status based on expiry date.
        
        Args:
            expiry_date: Date object representing document expiry
            
        Returns:
            str: "RED" if expired or expiring within 30 days, "GREEN" otherwise
            
        Requirements:
            - 5.3: Mark documents as RED if expired or expiring within 30 days
            - 5.4: Mark documents as GREEN if valid for more than 30 days
        """
        if not expiry_date:
            return "RED"
        
        today = datetime.now().date()
        threshold_date = today + timedelta(days=30)
        
        # RED if expired or expiring within 30 days
        if expiry_date <= threshold_date:
            return "RED"
        
        # GREEN if valid for more than 30 days
        return "GREEN"
    
    @staticmethod
    def calculate_subcontractor_status(documents):
        """
        Calculate overall compliance status for a subcontractor.
        
        Args:
            documents: List of ComplianceDocumentORM objects
            
        Returns:
            str: "RED" if any document is RED, "GREEN" if all are GREEN
        """
        if not documents:
            return "RED"
        
        for doc in documents:
            if ComplianceService.calculate_status(doc.expiry_date) == "RED":
                return "RED"
        
        return "GREEN"
