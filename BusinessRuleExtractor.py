import ollama

from LLM import LLM
from MistralModel import MistralModel
from OllamaModel import OllamaModel


class BusinessRuleExtractor:

    def __init__(self, llm: LLM):
        self.business_rules = []
        self.llm = llm
        self.systemPrompt1 = "You are an expert in legal document structuring and segmentation"

        self.prompt1 = ("Please divide the provided text into meaningful sections based on content and context. "
                        "Use the '#' symbol to separate each section. Focus on identifying distinct topics, legal clauses, or thematic shifts to ensure each segment"
                        " is coherent and self-contained.")

        self.systemPrompt2 = "You are an expert in legal document analysis and rule extraction. Your task is to extract rules from legal text segments and represent them in Prolog format. Each rule must adhere to the following conventions: \n\n\
    1. Use meaningful predicate names derived from the action or obligation described in the rule. Use camelCase for predicates.\n\
    2. Represent entities and conditions clearly as Prolog arguments or conditions. Use variables like Person, Transaction, or Entity as placeholders.\n\
    3. Use ':-' to define implications ('if'), ',' for logical AND, and ';' for logical OR.\n\
    4. Label sections with the heading from the input text as comments.\n\
    5. Ensure all Prolog rules are syntactically valid and logically consistent.\n\n\
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n\
% Facts and Predicates (placeholders for actual system data) \n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% \n\
\n\
% Example entities:\n\
% customer(CustomerID)\n\
% employee(EmployeeID)\n\
% vendor(VendorID)\n\
% transaction(TransactionID, Amount)\n\
% loan_applicant(ApplicantID)\n\
% expense_report(ReportID, SubmitterEmployeeID)\n\
% purchase(CustomerID, PurchaseID, PurchaseDate)\n\
% refund_request(CustomerID, PurchaseID, RequestDate)\n\
% discount(DiscountPercent)\n\
% terms_agreement(CustomerID)\n\
% vetted(VendorID)\n\
% approved_by_procurement(VendorID)\n\
% credit_score(ApplicantID, Score)\n\
% valid_id(CustomerID)\n\
% days_between(Date1, Date2, Days)\n\
% end_of_month(Date)\n\
\n\
% Additional utility predicates for encryption, etc., would also be defined.\n \
        % encrypt(Data, EncryptedData)\n \
        % store(EncryptedData)\n \
        % transmit(EncryptedData)\n \
 \
 \
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
% Rules Implementing the Policies\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
\n\
% 1. Customers must provide valid identification before opening an account.\n\
%    A customer can open an account only if they have a valid ID.\n\
can_open_account(CustomerID) :-\n\
customer(CustomerID),\n\
valid_id(CustomerID).\n\
\n\
% 2. All transactions above $10,000 must be reported to the compliance department.\n\
%    For a given transaction, check amount and determine if it needs reporting.\n\
report_to_compliance(TransactionID) :-\n\
transaction(TransactionID, Amount),\n\
Amount > 10000.\n\
\n\
% 3. Loan applications can only be processed if the applicant’s credit score >= 650.\n\
can_process_loan(ApplicantID) :-\n\
loan_applicant(ApplicantID),\n\
credit_score(ApplicantID, Score),\n\
Score >= 650.\n\
\n\
% 4. Employees are not allowed to approve their own expense reports.\n\
%    An employee can approve an expense report only if they are not the submitter.\n\
can_approve_expense(EmployeeID, ReportID) :-\n\
expense_report(ReportID, Submitter),\n\
EmployeeID \= Submitter.\n\
\n\
% 5. Refunds are only issued if the request is made within 30 days of the purchase date.\n\
eligible_for_refund(CustomerID, PurchaseID) :-\n\
purchase(CustomerID, PurchaseID, PurchaseDate),\n\
refund_request(CustomerID, PurchaseID, RequestDate),\n\
days_between(PurchaseDate, RequestDate, Days),\n\
Days =< 30.\n\
\n\
% 6. A manager must approve any discount greater than 20%.\n\
%    If a discount is > 20, we require manager_approval(…).\n\
needs_manager_approval(Discount) :-\n\
Discount > 20.\n\
\n\
% 7. Customers must agree to the terms and conditions before using the service.\n\
can_use_service(CustomerID) :-\n\
customer(CustomerID),\n\
terms_agreement(CustomerID).\n\
\n\
% 8. All customer data must be encrypted when stored or transmitted.\n\
%    These rules illustrate that data operations require encryption.\n\
store_customer_data(CustomerID, Data) :-\n\
customer(CustomerID),\n\
encrypt(Data, EncryptedData),\n\
store(EncryptedData).\n\
\n\
transmit_customer_data(CustomerID, Data) :-\n\
customer(CustomerID),\n\
encrypt(Data, EncryptedData),\n\
transmit(EncryptedData).\n\
\n\
% 9. Vendors must be vetted and approved by the procurement team before signing contracts.\n\
can_sign_contract(VendorID) :-\n\
vendor(VendorID),\n\
vetted(VendorID),\n\
approved_by_procurement(VendorID).\n\
\n\
% 10. Inventory checks must be conducted at the end of each month.\n\
%     This rule ensures inventory_check is performed only on end-of-month dates.\n\
conduct_inventory_check(Date) :-\n\
end_of_month(Date).\n\
\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
% The above provides a logical framework. Data (facts) about customers,\n\
% transactions, etc., would be added separately. For example:\n\
%\n\
% customer(cust123).\n\
% valid_id(cust123).\n\
% terms_agreement(cust123).\n\
%\n\
% transaction(tx456, 15000).\n\
%\n\
% credit_score(applicant789, 700).\n\
%\n\
% ... and so forth.\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
% Example Facts Representing System Data\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
\n\
% Customers and their valid IDs\n\
customer(cust001).\n\
customer(cust002).\n\
valid_id(cust001). \n\
% cust001 provided a valid ID\n\
% cust002 does not have valid_id fact, so they do not meet that requirement\n\
\n\
% Terms agreements\n\
terms_agreement(cust001). % cust001 agreed to terms\n\
\n\
% Transactions\n\
transaction(tx001, 5000).\n\
transaction(tx002, 20000).\n\
\n\
% Employees\n\
employee(emp100).\n\
employee(emp200).\n\
\n\
% Expense reports\n\
expense_report(rpt001, emp100).  % This report was submitted by emp100\n\
expense_report(rpt002, emp200).\n\
\n\
% Loan applicants and credit scores\n\
loan_applicant(appA).\n\
loan_applicant(appB).\n\
credit_score(appA, 700).\n\
credit_score(appB, 600).\n\
\n\
% Purchases and Refund Requests\n\
% Assume dates are encoded as date(Year, Month, Day)\n\
purchase(cust001, pur001, date(2024,11,1)).\n\
purchase(cust002, pur002, date(2024,10,1)).\n\
\n\
refund_request(cust001, pur001, date(2024,11,15)).  % 14 days after purchase\n\
refund_request(cust002, pur002, date(2024,12,5)).   % More than 30 days later (approx. 65 days)\n\
\n\
% Utility predicate for calculating days between dates (stub/example)\n\
% In a real system, you'd implement date arithmetic or call a library.\n\
days_between(date(Y1,M1,D1), date(Y2,M2,D2), Days) :-\n\
% This is a simplified placeholder that does not do proper calendar math.\n\
% Let's just assume all months have 30 days for demonstration.\n\
TotalDays1 is (Y1 * 360) + (M1 * 30) + D1,\n\
TotalDays2 is (Y2 * 360) + (M2 * 30) + D2,\n\
Days is TotalDays2 - TotalDays1.\n\
\n\
% Discounts\n\
% Example: if a discount is 25, manager approval is needed.\n\
% (No facts needed if we just query the rule with a specific discount number.)\n\
\n\
% Vendors\n\
vendor(vendX).\n\
vendor(vendY).\n\
vetted(vendX).\n\
approved_by_procurement(vendX).\n\
% vendY is not vetted or approved.\n\
\n\
% Inventory checks at end of month\n\
% Assume we mark a date as end_of_month when it’s the last day of the month:\n\
end_of_month(date(2024,11,30)).\n\
end_of_month(date(2024,12,31)).\n\
\n\
% Encryption storage and transmit (stubs)\n\
encrypt(Data, EncryptedData) :- atom_concat('enc_', Data, EncryptedData).\n\
store(_EncryptedData).  % Stub: assume store always succeeds\n\
transmit(_EncryptedData). % Stub: assume transmit always succeeds\n\
\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
% Example Queries and Their Expected Results\n\
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\
\n\
% 1. Can cust001 open an account?\n\
% Query:\n\
% ?- can_open_account(cust001).\n\
% Expected: true (because valid_id(cust001) is given)\n\
\n\
% 2. Which transactions must be reported to compliance?\n\
% Query:\n\
% ?- report_to_compliance(TxID).\n\
% Expected: TxID = tx002 (since tx002 amount is 20000 > 10000)\n\
\n\
% 3. Which loan applicants can be processed?\n\
% Query:\n\
% ?- can_process_loan(Applicant).\n\
% Expected: Applicant = appA (since appA has credit score 700 >= 650, appB has only 600)\n\
\n\
% 4. Can emp100 approve rpt001?\n\
% Query:\n\
% ?- can_approve_expense(emp100, rpt001).\n\
% Expected: false (because emp100 is the submitter of rpt001, so they can’t approve it)\n\
%\n\
% Can emp100 approve rpt002?\n\
% ?- can_approve_expense(emp100, rpt002).\n\
% Expected: true (because emp100 != emp200, so no conflict)\n\
\n\
% 5. Is cust001 eligible for a refund for purchase pur001?\n\
% Query:\n\
% ?- eligible_for_refund(cust001, pur001).\n\
% Expected: true (refund requested within 30 days)\n\
%\n\
% Is cust002 eligible for a refund for purchase pur002?\n\
% ?- eligible_for_refund(cust002, pur002).\n\
% Expected: false (request is made too late)\n\
\n\
% 6. Does a 25% discount need manager approval?\n\
% Query:\n\
% ?- needs_manager_approval(25).\n\
% Expected: true (25 > 20)\n\
\n\
% 7. Can cust001 use the service?\n\
% Query:\n\
% ?- can_use_service(cust001).\n\
% Expected: true (cust001 agreed to terms)\n\
\n\
% Can cust002 use the service?\n\
% ?- can_use_service(cust002).\n\
% Expected: false (no terms_agreement for cust002)\n\
\n\
% 8. Storing and transmitting customer data (just an example)\n\
% Query:\n\
% ?- store_customer_data(cust001, 'sensitive_info').\n\
% Expected: true (data gets encrypted and stored)\n\
%\n\
% ?- transmit_customer_data(cust001, 'sensitive_info').\n\
% Expected: true (data gets encrypted and transmitted)\n\
\n\
% 9. Can vendX sign a contract?\n\
% Query:\n\
% ?- can_sign_contract(vendX).\n\
% Expected: true (vetted and approved)\n\
%\n\
% Can vendY sign a contract?\n\
% ?- can_sign_contract(vendY).\n\
% Expected: false (not vetted or approved)\n\
\n\
% 10. Conducting inventory checks at the end of each month\n\
% Query:\n\
% ?- conduct_inventory_check(date(2024,11,30)).\n\
% Expected: true\n\
%\n\
% ?- conduct_inventory_check(date(2024,11,29)).\n\
% Expected: false (not end_of_month)"

        self.prompt2 = "From the following text segment, extract all rules in Prolog format"

    def extract_business_rules_from_document(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # extract the business rules from the text
        segments = model.segment_text(text, self.prompt1,self.systemPrompt1)
        extracted_rules = []
        for segment in segments:
            extracted_rules.append(model.extract_rules_from_text(segment, self.prompt2,self.systemPrompt2))

        return extracted_rules

    def transalte_document_to_english(self, text):
        # get the correct LLM model based on the LLM enum
        model = self.get_model()
        # translate the document to english
        return model.translate_document_to_english(text)

    def get_model(self):
        if self.llm == LLM.OLLAMA:
            return OllamaModel()
        if self.llm == LLM.MISTRAL:
            return MistralModel()
        # Add other models as needed
        else:
            raise ValueError("Unsupported LLM model")

